def test_runtime_dependencies_importable() -> None:
    import pandas
    import pydeck
    import streamlit

    assert pandas.__version__
    assert pydeck.__version__
    assert streamlit.__version__