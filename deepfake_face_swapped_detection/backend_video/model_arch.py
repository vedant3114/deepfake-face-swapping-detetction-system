import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import math

# Configuration specific to your trained model
class Config:
    HIDDEN_DIM = 128
    SEQUENCE_LENGTH = 32
    IMG_SIZE = 112
    AUDIO_SAMPLE_RATE = 16000
    AUDIO_N_MELS = 64
    AUDIO_N_FFT = 1024
    DROPOUT_RATE = 0.5

config = Config()

# --- Copying Model Classes from your notebook ---

class AudioFeatureExtractor(nn.Module):
    def __init__(self, input_dim=config.AUDIO_N_MELS, hidden_dim=config.HIDDEN_DIM, num_layers=2):
        super(AudioFeatureExtractor, self).__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=(3, 3), padding=1), nn.BatchNorm2d(16), nn.ReLU(inplace=True), nn.MaxPool2d(2, 2), nn.Dropout2d(config.DROPOUT_RATE),
            nn.Conv2d(16, 32, kernel_size=(3, 3), padding=1), nn.BatchNorm2d(32), nn.ReLU(inplace=True), nn.MaxPool2d(2, 2), nn.Dropout2d(config.DROPOUT_RATE),
            nn.Conv2d(32, 64, kernel_size=(3, 3), padding=1), nn.BatchNorm2d(64), nn.ReLU(inplace=True), nn.AdaptiveAvgPool2d((2, 2))
        )
        self.temporal_dim = 64 * 2 * 2
        self.temporal_projection = nn.Linear(self.temporal_dim, hidden_dim)
        self.positional_encoding = self._create_positional_encoding(config.SEQUENCE_LENGTH, hidden_dim)
        encoder_layer = nn.TransformerEncoderLayer(d_model=hidden_dim, nhead=4, dim_feedforward=hidden_dim * 2, dropout=config.DROPOUT_RATE, activation='gelu', batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.output_projection = nn.Sequential(nn.LayerNorm(hidden_dim), nn.Dropout(config.DROPOUT_RATE), nn.Linear(hidden_dim, hidden_dim))

    def _create_positional_encoding(self, seq_len, d_model):
        pe = torch.zeros(seq_len, d_model)
        position = torch.arange(0, seq_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        # --- FIX: Register as buffer for proper device handling ---
        self.register_buffer('_pe', pe.unsqueeze(0), persistent=False)
        return pe.unsqueeze(0)

    def forward(self, audio_input):
        batch_size, seq_len, n_mels, time_frames = audio_input.shape
        audio_reshaped = audio_input.reshape(-1, 1, n_mels, time_frames)
        conv_features = self.conv_layers(audio_reshaped).reshape(-1, self.temporal_dim)
        temporal_features = self.temporal_projection(conv_features).reshape(batch_size, seq_len, -1)
        # --- FIX: Use device-aware positional encoding ---
        pos_encoding = self.positional_encoding[:, :seq_len, :].to(audio_input.device)
        output_features = self.output_projection(self.transformer_encoder(temporal_features + pos_encoding))
        return output_features

class AudioTemporalConsistencyModule(nn.Module):
    def __init__(self, feature_dim=256):
        super(AudioTemporalConsistencyModule, self).__init__()
        self.temporal_diff_encoder = nn.Sequential(
            nn.Linear(feature_dim * 2, feature_dim), nn.LayerNorm(feature_dim), nn.GELU(), nn.Dropout(0.2),
            nn.Linear(feature_dim, feature_dim // 2), nn.LayerNorm(feature_dim // 2), nn.GELU(), nn.Linear(feature_dim // 2, 1)
        )
    def forward(self, audio_features):
        batch_size, seq_len, _ = audio_features.shape
        consistency_scores = []
        for i in range(seq_len - 1):
            frame_pair = torch.cat([audio_features[:, i, :], audio_features[:, i + 1, :]], dim=1)
            consistency_scores.append(torch.sigmoid(self.temporal_diff_encoder(frame_pair)))
        return torch.cat(consistency_scores, dim=1)

class SpatialAttentionModule(nn.Module):
    def __init__(self, in_channels, reduction_ratio=16):
        super(SpatialAttentionModule, self).__init__()
        self.channel_attention = nn.Sequential(nn.AdaptiveAvgPool2d(1), nn.Conv2d(in_channels, in_channels // reduction_ratio, 1), nn.ReLU(inplace=True), nn.Conv2d(in_channels // reduction_ratio, in_channels, 1), nn.Sigmoid())
        self.spatial_attention = nn.Sequential(nn.Conv2d(2, 1, kernel_size=7, padding=3), nn.Sigmoid())
    def forward(self, x):
        x = x * self.channel_attention(x)
        spatial_input = torch.cat([torch.mean(x, dim=1, keepdim=True), torch.max(x, dim=1, keepdim=True)[0]], dim=1)
        return x * self.spatial_attention(spatial_input)

class VideoFeatureExtractor(nn.Module):
    def __init__(self, hidden_dim=config.HIDDEN_DIM, num_layers=2):
        super(VideoFeatureExtractor, self).__init__()
        resnet = torchvision.models.resnet18(weights=None)
        self.backbone = nn.Sequential(*list(resnet.children())[:-2])
        self.spatial_attention = SpatialAttentionModule(512)
        self.adaptive_pool = nn.AdaptiveAvgPool2d((2, 2))
        self.spatial_dim = 512 * 2 * 2
        self.temporal_projection = nn.Linear(self.spatial_dim, hidden_dim)
        self.positional_encoding = self._create_positional_encoding(config.SEQUENCE_LENGTH, hidden_dim)
        encoder_layer = nn.TransformerEncoderLayer(d_model=hidden_dim, nhead=4, dim_feedforward=hidden_dim * 2, dropout=config.DROPOUT_RATE, activation='gelu', batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.output_projection = nn.Sequential(nn.LayerNorm(hidden_dim), nn.Dropout(config.DROPOUT_RATE), nn.Linear(hidden_dim, hidden_dim))

    def _create_positional_encoding(self, seq_len, d_model):
        pe = torch.zeros(seq_len, d_model)
        position = torch.arange(0, seq_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        return pe.unsqueeze(0)

    def forward(self, video_input):
        batch_size, seq_len, c, h, w = video_input.shape
        video_reshaped = video_input.reshape(-1, c, h, w)
        spatial_features = self.backbone(video_reshaped)
        attended_features = self.spatial_attention(spatial_features)
        pooled_features = self.adaptive_pool(attended_features)
        flattened = pooled_features.reshape(-1, self.spatial_dim)
        temporal_features = self.temporal_projection(flattened).reshape(batch_size, seq_len, -1)
        # --- FIX: Use device-aware positional encoding ---
        pos_encoding = self.positional_encoding[:, :seq_len, :].to(video_input.device)
        return self.output_projection(self.transformer_encoder(temporal_features + pos_encoding))

class VideoTemporalConsistencyModule(nn.Module):
    def __init__(self, feature_dim=256):
        super(VideoTemporalConsistencyModule, self).__init__()
        self.frame_diff_encoder = nn.Sequential(nn.Linear(feature_dim * 2, feature_dim), nn.LayerNorm(feature_dim), nn.GELU(), nn.Dropout(0.2), nn.Linear(feature_dim, feature_dim // 2), nn.LayerNorm(feature_dim // 2), nn.GELU(), nn.Linear(feature_dim // 2, 1))
        self.motion_encoder = nn.Sequential(nn.Linear(feature_dim * 3, feature_dim), nn.LayerNorm(feature_dim), nn.GELU(), nn.Dropout(0.2), nn.Linear(feature_dim, feature_dim // 2), nn.LayerNorm(feature_dim // 2), nn.GELU(), nn.Linear(feature_dim // 2, 1))

    def forward(self, video_features):
        batch_size, seq_len, _ = video_features.shape
        frame_scores, motion_scores = [], []
        for i in range(seq_len - 1):
            frame_scores.append(torch.sigmoid(self.frame_diff_encoder(torch.cat([video_features[:, i, :], video_features[:, i + 1, :]], dim=1))))
            if i < seq_len - 2:
                motion_scores.append(torch.sigmoid(self.motion_encoder(torch.cat([video_features[:, i, :], video_features[:, i + 1, :], video_features[:, i + 2, :]], dim=1))))
        
        frame_stack = torch.cat(frame_scores, dim=1)
        motion_stack = torch.cat(motion_scores, dim=1) if motion_scores else torch.full_like(frame_stack, 0.5)
        motion_stack = F.pad(motion_stack, (0, 1), value=0.5)
        return (frame_stack + motion_stack) / 2

class CrossModalAttention(nn.Module):
    def __init__(self, feature_dim=256, num_heads=8, dropout=0.1):
        super(CrossModalAttention, self).__init__()
        self.num_heads, self.head_dim = num_heads, feature_dim // num_heads
        self.query_proj = nn.Linear(feature_dim, feature_dim)
        self.key_proj = nn.Linear(feature_dim, feature_dim)
        self.value_proj = nn.Linear(feature_dim, feature_dim)
        self.output_proj = nn.Linear(feature_dim, feature_dim)
        self.dropout = nn.Dropout(dropout)
        self.layer_norm = nn.LayerNorm(feature_dim)

    def forward(self, query, key_value):
        b, s, f = query.shape
        Q = self.query_proj(query).reshape(b, s, self.num_heads, self.head_dim).transpose(1, 2)
        K = self.key_proj(key_value).reshape(b, s, self.num_heads, self.head_dim).transpose(1, 2)
        V = self.value_proj(key_value).reshape(b, s, self.num_heads, self.head_dim).transpose(1, 2)
        attn = F.softmax(torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.head_dim), dim=-1)
        out = torch.matmul(self.dropout(attn), V).transpose(1, 2).contiguous().reshape(b, s, f)
        return self.layer_norm(self.output_proj(out) + query), attn

class TemporalAggregator(nn.Module):
    def __init__(self, feature_dim):
        super(TemporalAggregator, self).__init__()
        self.attention_aggregator = nn.Sequential(nn.Linear(feature_dim, feature_dim // 2), nn.Tanh(), nn.Linear(feature_dim // 2, 1), nn.Softmax(dim=1))
        self.pooling_weights = nn.Parameter(torch.ones(4) / 4)

    def forward(self, features):
        att_w = self.attention_aggregator(features)
        att_p = torch.sum(features * att_w, dim=1)
        return sum(w * p for w, p in zip(self.pooling_weights, [att_p, torch.mean(features, dim=1), torch.max(features, dim=1)[0], features[:, -1, :]]))

class MultiModalFusionNetwork(nn.Module):
    def __init__(self, feature_dim=config.HIDDEN_DIM, num_classes=2, num_fusion_layers=1):
        super(MultiModalFusionNetwork, self).__init__()
        
        self.audio_to_video_attention = nn.ModuleList([
            CrossModalAttention(feature_dim, num_heads=4, dropout=config.DROPOUT_RATE) 
            for _ in range(num_fusion_layers)
        ])
        self.video_to_audio_attention = nn.ModuleList([
            CrossModalAttention(feature_dim, num_heads=4, dropout=config.DROPOUT_RATE) 
            for _ in range(num_fusion_layers)
        ])
        self.self_attention = nn.ModuleList([
            nn.MultiheadAttention(feature_dim, num_heads=4, dropout=config.DROPOUT_RATE, batch_first=True) 
            for _ in range(2)
        ])
        
        self.fusion_strategies = nn.ModuleDict({
            'concat': nn.Sequential(
                nn.Linear(feature_dim * 2, feature_dim), 
                nn.LayerNorm(feature_dim), 
                nn.GELU(), 
                nn.Dropout(config.DROPOUT_RATE)
            ),
            'attention': nn.Sequential(
                nn.Linear(feature_dim * 2, feature_dim), 
                nn.Tanh(), 
                nn.Dropout(config.DROPOUT_RATE), 
                nn.Linear(feature_dim, 1), 
                nn.Softmax(dim=1)
            )
        })
        
        self.temporal_aggregator = TemporalAggregator(feature_dim)
        
        self.classifier = nn.Sequential(
            nn.Linear(feature_dim * 2, feature_dim), 
            nn.LayerNorm(feature_dim), 
            nn.GELU(), 
            nn.Dropout(config.DROPOUT_RATE), 
            nn.Linear(feature_dim, num_classes)
        )
        
        self.audio_consistency_head = nn.Linear(feature_dim, 1)
        self.video_consistency_head = nn.Linear(feature_dim, 1)
        self.cross_modal_consistency_head = nn.Linear(feature_dim * 2, 1)

    def forward(self, audio, video):
        for i in range(len(self.audio_to_video_attention)):
            audio, _ = self.audio_to_video_attention[i](audio, video)
            video, _ = self.video_to_audio_attention[i](video, audio)
        
        audio_ref, _ = self.self_attention[0](audio, audio, audio)
        video_ref, _ = self.self_attention[1](video, video, video)
        
        # Fusion
        concat = self.fusion_strategies['concat'](torch.cat([audio_ref, video_ref], dim=-1))
        att_w = self.fusion_strategies['attention'](torch.cat([audio_ref, video_ref], dim=-1))
        att_fus = att_w * audio_ref + (1 - att_w) * video_ref
        
        final_features = torch.cat([self.temporal_aggregator(concat), self.temporal_aggregator(att_fus)], dim=-1)
        logits = self.classifier(final_features)
        
        audio_g, video_g = self.temporal_aggregator(audio_ref), self.temporal_aggregator(video_ref)
        
        consistency = {
            'audio_consistency': torch.sigmoid(self.audio_consistency_head(audio_g)),
            'video_consistency': torch.sigmoid(self.video_consistency_head(video_g)),
            'cross_modal_consistency': torch.sigmoid(
                self.cross_modal_consistency_head(torch.cat([audio_g, video_g], dim=-1))
            )
        }
        return logits, consistency, audio_ref, video_ref

class MultiModalDeepfakeDetector(nn.Module):
    def __init__(self, hidden_dim=config.HIDDEN_DIM, num_classes=2):
        super(MultiModalDeepfakeDetector, self).__init__()
        self.audio_extractor = AudioFeatureExtractor(hidden_dim=hidden_dim)
        self.audio_consistency = AudioTemporalConsistencyModule(hidden_dim)
        self.video_extractor = VideoFeatureExtractor(hidden_dim=hidden_dim)
        self.video_consistency = VideoTemporalConsistencyModule(hidden_dim)
        self.fusion_network = MultiModalFusionNetwork(feature_dim=hidden_dim, num_classes=num_classes)

    def forward(self, audio, video, return_features=False):
        audio_feat = self.audio_extractor(audio)
        video_feat = self.video_extractor(video)
        audio_cons = self.audio_consistency(audio_feat)
        video_cons = self.video_consistency(video_feat)
        logits, consistency_scores, _, _ = self.fusion_network(audio_feat, video_feat)
        
        outputs = {
            'logits': logits,
            'consistency_scores': consistency_scores,
            'audio_temporal_consistency': audio_cons,
            'video_temporal_consistency': video_cons
        }
        return outputs