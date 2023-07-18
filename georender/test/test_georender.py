import pytest
from ..georender import call_function, run_georender_pipeline_point

def test_run_georender_point():
    call_function("run_georender_pipeline_point", ["43", "34", "testing"])
