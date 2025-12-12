"""
Template for model definition. Copy this file to `backend/app/model_def.py` and implement
`build_model()` to return an instantiated PyTorch `nn.Module` matching your checkpoint.

Example usage:
    def build_model():
        model = MyModel(...)  # your model class
        return model

Make sure the model's state_dict keys match the checkpoint.
"""

def build_model():
    raise NotImplementedError("Replace this template with your model architecture and return the model instance from build_model().")
