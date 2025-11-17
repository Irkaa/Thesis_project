"""
Model loading and caching for YOLO and ArcFace.
Implements singleton pattern for efficient model reuse.
"""
import onnxruntime as ort
import logging
from app.utils.config import YOLO_MODEL_PATH, ARCFACE_MODEL_PATH

logger = logging.getLogger(__name__)

# ========== GLOBAL SINGLETONS ==========
_yolo_session = None
_yolo_input_name = None
_yolo_input_size = None
_yolo_output_format = None

_arcface_session = None
_arcface_input_name = None
_arcface_input_size = None


# ========== YOLO MODEL ==========
def get_yolo_session():
    """Lazy load YOLO model (singleton pattern)."""
    global _yolo_session, _yolo_input_name, _yolo_input_size
    if _yolo_session is None:
        _yolo_session = ort.InferenceSession(
            YOLO_MODEL_PATH,
            providers=["CPUExecutionProvider"]
        )
        # Cache input name and size
        input_meta = _yolo_session.get_inputs()[0]
        _yolo_input_name = input_meta.name
        # Extract input size from shape: typically [batch, 3, height, width]
        shape = input_meta.shape
        if len(shape) == 4:
            _yolo_input_size = shape[2]  # Assume square input (height == width)
            logger.info(f"YOLO input size: {_yolo_input_size}x{_yolo_input_size}")
        else:
            _yolo_input_size = 640  # Fallback to default
            logger.warning(f"Unexpected YOLO input shape: {shape}, defaulting to 640")
    return _yolo_session


def get_yolo_input_name():
    """Get cached YOLO input name."""
    if _yolo_input_name is None:
        get_yolo_session()  # Trigger lazy load
    return _yolo_input_name


def get_yolo_input_size():
    """Get cached YOLO input size."""
    if _yolo_input_size is None:
        get_yolo_session()  # Trigger lazy load
    return _yolo_input_size


def get_yolo_output_format():
    """Get cached YOLO output format."""
    return _yolo_output_format


def set_yolo_output_format(format_type: str):
    """Set YOLO output format after inspection."""
    global _yolo_output_format
    _yolo_output_format = format_type


def inspect_yolo_model():
    """
    Inspect YOLO model at startup to understand output format.
    Logs input/output shapes for debugging.
    """
    session = get_yolo_session()

    # Log input info
    inputs = session.get_inputs()
    logger.info(f"YOLO Model - Inputs: {len(inputs)}")
    for inp in inputs:
        logger.info(f"  - {inp.name}: shape={inp.shape}, type={inp.type}")

    # Log output info
    outputs = session.get_outputs()
    logger.info(f"YOLO Model - Outputs: {len(outputs)}")
    for out in outputs:
        logger.info(f"  - {out.name}: shape={out.shape}, type={out.type}")

    # Determine output format based on shape
    if len(outputs) == 1:
        shape = outputs[0].shape
        logger.info(f"Single output detected: {shape}")
        set_yolo_output_format("single")
    elif len(outputs) == 2:
        logger.info("Dual output detected (likely boxes + scores)")
        set_yolo_output_format("dual")
    else:
        logger.warning(f"Unexpected output count: {len(outputs)}")
        set_yolo_output_format("unknown")


# ========== ARCFACE MODEL ==========
def get_arcface_session():
    """Lazy load ArcFace model (singleton pattern)."""
    global _arcface_session, _arcface_input_name, _arcface_input_size
    if _arcface_session is None:
        _arcface_session = ort.InferenceSession(
            ARCFACE_MODEL_PATH,
            providers=["CPUExecutionProvider"]
        )
        # Cache input name and size
        input_meta = _arcface_session.get_inputs()[0]
        _arcface_input_name = input_meta.name
        # Extract input size from shape: typically [batch, 3, height, width]
        shape = input_meta.shape
        if len(shape) == 4:
            _arcface_input_size = shape[2]  # Assume square input
            logger.info(f"ArcFace input size: {_arcface_input_size}x{_arcface_input_size}")
        else:
            _arcface_input_size = 112  # Fallback to default
            logger.warning(f"Unexpected ArcFace input shape: {shape}, defaulting to 112")
    return _arcface_session


def get_arcface_input_name():
    """Get cached ArcFace input name."""
    if _arcface_input_name is None:
        get_arcface_session()  # Trigger lazy load
    return _arcface_input_name


def get_arcface_input_size():
    """Get cached ArcFace input size."""
    if _arcface_input_size is None:
        get_arcface_session()  # Trigger lazy load
    return _arcface_input_size
