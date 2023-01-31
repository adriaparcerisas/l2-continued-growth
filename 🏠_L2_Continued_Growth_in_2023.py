#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

# In[8]:


import streamlit as st
import pandas as pd
import numpy as np
from shroomdk import ShroomDK
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker
import numpy as np
import altair as alt
sdk = ShroomDK("7bfe27b2-e726-4d8d-b519-03abc6447728")


# In[9]:


st.title('Ethereum L2 Ecosystem Dashboard')


# In[10]:


st.markdown("Layer 2 is an independent blockchain that extends Ethereum.  A layer 2 blockchain communicates regularly with Ethereum to ensure that it has similar guarantees of security and decentralisation. All this requires no changes to the layer 1 protocol (Ethereum) so layer 1 takes care of security, data availability and decentralisation, while layer 2 takes care of scaling [1](https://ethereum.org/en/layer-2).") 
st.markdown("So we can say that layer 2 removes the transactional load from layer 1 and returns the completed proofs to layer 1. By removing this transactional load from layer 1, the base layer becomes less congested and everything becomes more scalable and faster.")
st.markdown("The holidays and New Year are often chaotic in the crypto and DEFI space, as users make a spree of new transactions and wallets as they receive (and give) some cash and coins as holiday gifts. Has this flurry of winter activity impacted the ecosystem? Are users creating new wallets or buying tokens with their newfound holiday wealth? Are they staking all those new tokens once they get them? Or are they selling tokens to pay for their own gifts and holiday travel?")

# In[11]:
st.markdown("The main idea of this app is to show an overview of how the entire Ethereum L2 community respond to this new 2023 year and how all sectors changed during this first days. You can find information about each different section by navigating on the sidebar pages.")


# In[12]:


st.markdown("These includes:") 
st.markdown("1. **_Main Layer 2 activity_**") 
st.markdown("2. **_New user Layer 2 activity_**")


# In[ ]:




