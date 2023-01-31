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


st.title('Ethereum L2 Ecosystem in 2023')


# In[10]:


st.markdown("Layer 2 is an independent blockchain that extends Ethereum.  A layer 2 blockchain communicates regularly with Ethereum to ensure that it has similar guarantees of security and decentralisation. All this requires no changes to the layer 1 protocol (Ethereum) so layer 1 takes care of security, data availability and decentralisation, while layer 2 takes care of scaling [1](https://ethereum.org/en/layer-2).") 
st.markdown("So we can say that layer 2 removes the transactional load from layer 1 and returns the completed proofs to layer 1. By removing this transactional load from layer 1, the base layer becomes less congested and everything becomes more scalable and faster.")
st.markdown('As noted in a recent piece in Cointelegraph, _Ethereum layer-2 networks, such as Polygon, Arbitrum, and Optimism,  have gone through an explosive growth phase over the past couple of months, a trend that is set to continue in 2023._')
st.markdown('Specifically, there’s been a notable increase in the amount of daily active users, volume traded, and more. Will this growth continue into the new year? Or will L2 growth stagnate as 2023 continues to progress?')


# In[11]:
st.markdown("The main idea of this app is to show an overview of how the entire Ethereum L2 community respond to this new 2023 year and how all sectors changed during this first days in comparison to the previous 2 months when the activity surged. You can find information about each different section by navigating on the sidebar pages.")


# In[12]:


st.markdown("These includes:") 
st.markdown("1. **_Main Layer 2 activity_**") 
st.markdown("2. **_Layer 2 swapping activity_**")
st.markdown("3. **_Layer 2 NFT activity_**")
st.markdown("4. **_Layer 2 DeFi activity_**")



# In[ ]:




