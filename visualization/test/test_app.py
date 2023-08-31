import pytest
import streamlit as st

def test_kafka_discord_producer():
    Xcoord = "34.0"
    Ycoord = "21.0"
    username = "Dhruv"
    ipfsDetails = "bafybeibbtseqjgu72lmehn2y2b772wvr36othnc4rpzu6z3v2gfsjy3ew4"
    assert kafka_producer_message(Xcoord=Xcoord, Ycoord=Ycoord, username=username, ipfsDetails=ipfsDetails) is True
    
    