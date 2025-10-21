import base64
import io
import polars as pl

def df_to_base64_ipc(df: pl.DataFrame) -> str:
    """Serialize a Polars DF to IPC (Arrow) and return base64 string."""
    buf = io.BytesIO()
    df.write_ipc(buf)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")

def df_from_base64_ipc(b64str: str) -> pl.DataFrame:
    """Deserialize base64 IPC string back to a Polars DataFrame."""
    raw = base64.b64decode(b64str)
    return pl.read_ipc(io.BytesIO(raw))