#!/usr/bin/env python
# coding: utf-8

# In[13]:


#!/usr/bin/env python
# coding: utf-8

# In[18]:


import streamlit as st
import pandas as pd
import numpy as np
from shroomdk import ShroomDK
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker
import numpy as np
import plotly.express as px
sdk = ShroomDK("7bfe27b2-e726-4d8d-b519-03abc6447728")


# In[19]:


st.title('Ethereum L2 activity since 2023')


# In[20]:


st.markdown('This app shows the basic activity trends on **Ethereum L2** ecosystems since 2023. It is intended to provide an overview of the current activity on Layer 2 platforms.')


# In[5]:


st.markdown('To do that, we are gonna track the basic activity metrics registered on each L2 chain since the start of this year such as:') 
st.write('- Evolution of transactions, transactors and transactions per user')
st.write('- Evolution of NFT sales, buyers and buys per user')
st.write('- Evolution of DeFi transactions, DeFi users and DeFi transactions per user')
st.write('')


# In[10]:


sql = f"""
with 
t1 as (
SELECT
trunc(x.block_timestamp,'day') as date,
count(distinct x.tx_hash) as transactions,
count(distinct x.from_address) as active_users,
transactions/active_users as avg_tx_per_user,
sum(tx_fee) as fees,
avg(tx_fee) as avg_tx_fee
  from arbitrum.core.fact_transactions x
  where x.block_timestamp>='2023-01-01'
  group by 1
  ),
  t2 as (
  select
trunc(y.block_timestamp,'day') as date,
count(distinct y.tx_hash) as swaps,
count(distinct ORIGIN_FROM_ADDRESS) as swappers,
swaps/swappers as avg_swaps_per_swapper
  from arbitrum.core.fact_event_logs y
  where y.block_timestamp>='2023-01-01'
  and event_name='Swap'
  group by 1
  ),
  t3 as (
  select
  trunc(z.block_timestamp,'day') as date,
count(distinct z.tx_hash) as nft_sales,
count(distinct z.origin_from_address) as nft_buyers,
nft_sales/nft_buyers as nft_bought_per_user
  from arbitrum.core.fact_event_logs z
  join arbitrum.core.dim_labels l on z.contract_address=l.address
  where z.block_timestamp>='2023-01-01'
  and label_type='nft'
  group by 1
  ),
  t4 as (
  select
  trunc(z.block_timestamp,'day') as date,
count(distinct z.tx_hash) as defi_txs,
count(distinct z.origin_from_address) as defi_users,
defi_txs/defi_users as defi_txs_user
  from arbitrum.core.fact_event_logs z
  join arbitrum.core.dim_labels l on z.contract_address=l.address
  where z.block_timestamp>='2023-01-01'
  and label_type='defi'
  group by 1
  )
  SELECT
  t1.date, 
  transactions,sum(transactions) over (order by t1.date) as cum_transactions,
  active_users,sum(active_users) over (order by t1.date) as cum_users,
  avg_tx_per_user,
  fees,sum(fees) over (order by t1.date) as cum_fees,
  avg_tx_fee,
  swaps,sum(swaps) over (order by t1.date) as cum_swaps,
  swappers,sum(swappers) over (order by t1.date) as cum_swappers,
  avg_swaps_per_swapper,
  nft_sales,sum(nft_sales) over (order by t1.date) as cum_sales,
  nft_buyers,sum(nft_buyers) over (order by t1.date) as cum_buyers,
  nft_bought_per_user,
  defi_txs,sum(defi_txs) over (order by t1.date) as cum_defi_txs,
  defi_users,sum(defi_users) over (order by t1.date) as cum_defi_users,
  defi_txs_user
  from t1,t2,t3,t4 where t1.date=t2.date and t1.date=t3.date and t1.date=t4.date
order by 1 asc 
"""

sql2 = f"""
with 
t12 as (
SELECT
trunc(x.block_timestamp,'day') as date,
count(distinct x.tx_hash) as transactions,
count(distinct x.from_address) as active_users,
transactions/active_users as avg_tx_per_user,
sum(tx_fee) as fees,
avg(tx_fee) as avg_tx_fee
  from optimism.core.fact_transactions x
  where x.block_timestamp>='2023-01-01'
  group by 1
  ),
  t22 as (
  select
trunc(y.block_timestamp,'day') as date,
count(distinct y.tx_hash) as swaps,
count(distinct ORIGIN_FROM_ADDRESS) as swappers,
swaps/swappers as avg_swaps_per_swapper
  from optimism.core.fact_event_logs y
  where y.block_timestamp>='2023-01-01'
  and event_name='Swap'
  group by 1
  ),
  t32 as (
  select
  trunc(z.block_timestamp,'day') as date,
count(distinct z.tx_hash) as nft_sales,
count(distinct z.origin_from_address) as nft_buyers,
nft_sales/nft_buyers as nft_bought_per_user
  from optimism.core.fact_event_logs z
  join optimism.core.dim_labels l on z.contract_address=l.address
  where z.block_timestamp>='2023-01-01'
  and label_type='nft'
  group by 1
  ),
  t42 as (
  select
  trunc(z.block_timestamp,'day') as date,
count(distinct z.tx_hash) as defi_txs,
count(distinct z.origin_from_address) as defi_users,
defi_txs/defi_users as defi_txs_user
  from optimism.core.fact_event_logs z
  join optimism.core.dim_labels l on z.contract_address=l.address
  where z.block_timestamp>='2023-01-01'
  and label_type='defi'
  group by 1
  )
  SELECT
  t12.date, 
  transactions,sum(transactions) over (order by t12.date) as cum_transactions,
  active_users,sum(active_users) over (order by t12.date) as cum_users,
  avg_tx_per_user,
  fees,sum(fees) over (order by t12.date) as cum_fees,
  avg_tx_fee,
  swaps,sum(swaps) over (order by t12.date) as cum_swaps,
  swappers,sum(swappers) over (order by t12.date) as cum_swappers,
  avg_swaps_per_swapper,
  nft_sales,sum(nft_sales) over (order by t12.date) as cum_sales,
  nft_buyers,sum(nft_buyers) over (order by t12.date) as cum_buyers,
  nft_bought_per_user,
  defi_txs,sum(defi_txs) over (order by t12.date) as cum_defi_txs,
  defi_users,sum(defi_users) over (order by t12.date) as cum_defi_users,
  defi_txs_user
  from t12,t22,t32,t42 where t12.date=t22.date and t12.date=t32.date and t12.date=t42.date
order by 1 asc 
"""

sql3 = f"""
with 
t13 as (
SELECT
trunc(x.block_timestamp,'day') as date,
count(distinct x.tx_hash) as transactions,
count(distinct x.from_address) as active_users,
transactions/active_users as avg_tx_per_user,
sum(tx_fee) as fees,
avg(tx_fee) as avg_tx_fee
  from polygon.core.fact_transactions x
  where x.block_timestamp>='2023-01-01'
  group by 1
  ),
  t23 as (
  select
trunc(y.block_timestamp,'day') as date,
count(distinct y.tx_hash) as swaps,
count(distinct ORIGIN_FROM_ADDRESS) as swappers,
swaps/swappers as avg_swaps_per_swapper
  from polygon.core.fact_event_logs y
  where y.block_timestamp>='2023-01-01'
  and event_name='Swap'
  group by 1
  ),
  t33 as (
  select
  trunc(z.block_timestamp,'day') as date,
count(distinct z.tx_hash) as nft_sales,
count(distinct z.origin_from_address) as nft_buyers,
nft_sales/nft_buyers as nft_bought_per_user
  from polygon.core.fact_event_logs z
  join polygon.core.dim_labels l on z.contract_address=l.address
  where z.block_timestamp>='2023-01-01'
  and label_type='nft'
  group by 1
  ),
  t43 as (
  select
  trunc(z.block_timestamp,'day') as date,
count(distinct z.tx_hash) as defi_txs,
count(distinct z.origin_from_address) as defi_users,
defi_txs/defi_users as defi_txs_user
  from polygon.core.fact_event_logs z
  join polygon.core.dim_labels l on z.contract_address=l.address
  where z.block_timestamp>='2023-01-01'
  and label_type='defi'
  group by 1
  )
  SELECT
  t13.date, 
  transactions,sum(transactions) over (order by t13.date) as cum_transactions,
  active_users,sum(active_users) over (order by t13.date) as cum_users,
  avg_tx_per_user,
  fees,sum(fees) over (order by t13.date) as cum_fees,
  avg_tx_fee,
  swaps,sum(swaps) over (order by t13.date) as cum_swaps,
  swappers,sum(swappers) over (order by t13.date) as cum_swappers,
  avg_swaps_per_swapper,
  nft_sales,sum(nft_sales) over (order by t13.date) as cum_sales,
  nft_buyers,sum(nft_buyers) over (order by t13.date) as cum_buyers,
  nft_bought_per_user,
  defi_txs,sum(defi_txs) over (order by t13.date) as cum_defi_txs,
  defi_users,sum(defi_users) over (order by t13.date) as cum_defi_users,
  defi_txs_user
  from t13,t23,t33,t43 where t13.date=t23.date and t13.date=t33.date and t13.date=t43.date
order by 1 asc 
"""

# In[11]:


st.experimental_memo(ttl=21600)
@st.cache
def compute(a):
    data=sdk.query(a)
    return data

results = compute(sql)
df = pd.DataFrame(results.records)
df.info()

results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()

results3 = compute(sql3)
df3 = pd.DataFrame(results3.records)
df3.info()
#st.subheader('Terra general activity metrics regarding transactions')
#st.markdown('In this first part, we can take a look at the main activity metrics on Terra, where it can be seen how the number of transactions done across the protocol, as well as some other metrics such as fees and TPS.')


# In[22]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['transactions'],
                name='# of transactions',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_transactions'],
                name='# of transactions',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig1.update_layout(
    title='Daily Arbitrum transactions',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily transactions", secondary_y=False)
fig1.update_yaxes(title_text="Arbitrum transactions", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['transactions'],
                name='# of transactions',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_transactions'],
                name='# of transactions',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig2.update_layout(
    title='Daily Optimism transactions',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily transactions", secondary_y=False)
fig2.update_yaxes(title_text="Optimism transactions", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['transactions'],
                name='# of transactions',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_transactions'],
                name='# of transactions',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig3.update_layout(
    title='Polygon transactions',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Daily transactions", secondary_y=False)
fig3.update_yaxes(title_text="Polygon transactions", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily Arbitrum transactions", "Daily Optimism transactions", "Daily Polygon transactions"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[15]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['active_users'],
                name='Users',
                marker_color='rgb(132, 243, 132)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_users'],
                name='Users',
                marker_color='rgb(21, 174, 21)'
                , yaxis='y2'))

fig1.update_layout(
    title='Daily Arbitrum users',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily active users", secondary_y=False)
fig1.update_yaxes(title_text="Arbitrum active users", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['active_users'],
                name='Users',
                marker_color='rgb(132, 243, 132)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_users'],
                name='Users',
                marker_color='rgb(21, 174, 21)'
                , yaxis='y2'))

fig2.update_layout(
    title='Daily Optimism users',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily active users", secondary_y=False)
fig2.update_yaxes(title_text="Optimism active users", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['active_users'],
                name='Users',
                marker_color='rgb(132, 243, 132)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_users'],
                name='Users',
                marker_color='rgb(21, 174, 21)'
                , yaxis='y2'))

fig3.update_layout(
    title='Polygon active users',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Daily active users", secondary_y=False)
fig3.update_yaxes(title_text="Polygon active users", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily Arbitrum active users", "Daily Optimism active users", "Daily Polygon active users"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[16]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['swaps'],
                name='# of swaps',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_swaps'],
                name='# of swaps',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig1.update_layout(
    title='Arbitrum swaps',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily Arbitrum swaps", secondary_y=False)
fig1.update_yaxes(title_text="Total Arbitrum swaps", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['swaps'],
                name='# of swaps',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_swaps'],
                name='# of swaps',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig2.update_layout(
    title='Optimism swaps',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily Optimism swaps", secondary_y=False)
fig2.update_yaxes(title_text="Total Optimism swaps", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['swaps'],
                name='# of swaps',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_swaps'],
                name='# of swaps',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig3.update_layout(
    title='Polygon swaps',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Daily Polygon swaps", secondary_y=False)
fig3.update_yaxes(title_text="Total Polygon swaps", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily Arbitrum swaps", "Daily Optimism swaps", "Daily Polygon swaps"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
    
    
    
    
    # In[16]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['swappers'],
                name='# of swappers',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_swappers'],
                name='# of swappers',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig1.update_layout(
    title='Arbitrum swappers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily Arbitrum swappers", secondary_y=False)
fig1.update_yaxes(title_text="Total Arbitrum swappers", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['swappers'],
                name='# of swappers',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_swappers'],
                name='# of swappers',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig2.update_layout(
    title='Optimism swappers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily Optimism swappers", secondary_y=False)
fig2.update_yaxes(title_text="Total Optimism swappers", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['swappers'],
                name='# of swappers',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_swappers'],
                name='# of swappers',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig3.update_layout(
    title='Polygon swappers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Daily Polygon swappers", secondary_y=False)
fig3.update_yaxes(title_text="Total Polygon swappers", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily Arbitrum swappers", "Daily Optimism swappers", "Daily Polygon swappers"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


    
    
    


# In[16]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['nft_sales'],
                name='# of nft sales',
                marker_color='rgb(177, 128, 233)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_sales'],
                name='# of nft sales',
                marker_color='rgb(58, 7, 115)'
                , yaxis='y2'))

fig1.update_layout(
    title='Arbitrum NFT sales',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily Arbitrum sales", secondary_y=False)
fig1.update_yaxes(title_text="Total Arbitrum sales", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['nft_sales'],
                name='# of sales',
                marker_color='rgb(177, 128, 233)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_sales'],
                name='# of sales',
                marker_color='rgb(58, 7, 115)'
                , yaxis='y2'))

fig2.update_layout(
    title='Optimism sales',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily Optimism sales", secondary_y=False)
fig2.update_yaxes(title_text="Total Optimism sales", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['nft_sales'],
                name='# of sales',
                marker_color='rgb(177, 128, 233)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_sales'],
                name='# of sales',
                marker_color='rgb(58, 7, 115)'
                , yaxis='y2'))

fig3.update_layout(
    title='Polygon sales',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Daily Polygon sales", secondary_y=False)
fig3.update_yaxes(title_text="Total Polygon sales", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily Arbitrum sales", "Daily Optimism sales", "Daily Polygon sales"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
    
    
    
    
    # In[16]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['nft_buyers'],
                name='# of buyers',
                marker_color='rgb(177, 128, 233)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_buyers'],
                name='# of buyers',
                marker_color='rgb(58, 7, 115)'
                , yaxis='y2'))

fig1.update_layout(
    title='Daily Arbitrum buyers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily Arbitrum buyers", secondary_y=False)
fig1.update_yaxes(title_text="Total Arbitrum buyers", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['nft_buyers'],
                name='# of buyers',
                marker_color='rgb(177, 128, 233)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_buyers'],
                name='# of buyers',
                marker_color='rgb(58, 7, 115)'
                , yaxis='y2'))

fig2.update_layout(
    title='Daily Optimism buyers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily Optimism buyers", secondary_y=False)
fig2.update_yaxes(title_text="Total Optimism buyers", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['nft_buyers'],
                name='# of buyers',
                marker_color='rgb(177, 128, 233)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_buyers'],
                name='# of buyers',
                marker_color='rgb(58, 7, 115)'
                , yaxis='y2'))

fig3.update_layout(
    title='Polygon buyers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Daily Polygon buyers", secondary_y=False)
fig3.update_yaxes(title_text="Total Polygon buyers", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily Arbitrum buyers", "Daily Optimism buyers", "Daily Polygon buyers"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
    
    
  

fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['defi_txs'],
                name='# of transactions',
                marker_color='rgb(246, 147, 187)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_defi_txs'],
                name='# of transactions',
                marker_color='rgb(115, 61, 7)'
                , yaxis='y2'))

fig1.update_layout(
    title='Daily Arbitrum DeFi transactions',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily DeFi transactions", secondary_y=False)
fig1.update_yaxes(title_text="Arbitrum DeFi transactions", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['defi_txs'],
                name='# of transactions',
                marker_color='rgb(246, 147, 187)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_defi_txs'],
                name='# of transactions',
                marker_color='rgb(115, 61, 7)'
                , yaxis='y2'))

fig2.update_layout(
    title='Daily Optimism DeFi transactions',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily DeFi transactions", secondary_y=False)
fig2.update_yaxes(title_text="Optimism DeFi transactions", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['defi_txs'],
                name='# of transactions',
                marker_color='rgb(246, 147, 187)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_defi_txs'],
                name='# of transactions',
                marker_color='rgb(115, 61, 7)'
                , yaxis='y2'))

fig3.update_layout(
    title='Polygon DeFi transactions',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Daily DeFi transactions", secondary_y=False)
fig3.update_yaxes(title_text="Polygon DeFi transactions", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily Arbitrum DeFi transactions", "Daily Optimism DeFi transactions", "Daily Polygon DeFi transactions"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


    
    
    # In[16]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['defi_users'],
                name='# of users',
                marker_color='rgb(246, 147, 187)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_defi_users'],
                name='# of users',
                marker_color='rgb(115, 61, 7)'
                , yaxis='y2'))

fig1.update_layout(
    title='Arbitrum DeFi users',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily Arbitrum DeFi users", secondary_y=False)
fig1.update_yaxes(title_text="Total Arbitrum DeFi users", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['defi_users'],
                name='# of users',
                marker_color='rgb(246, 147, 187)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_defi_users'],
                name='# of users',
                marker_color='rgb(115, 61, 7)'
                , yaxis='y2'))

fig2.update_layout(
    title='Optimism DeFi users',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily Optimism DeFi users", secondary_y=False)
fig2.update_yaxes(title_text="Total Optimism DeFi users", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['defi_users'],
                name='# of users',
                marker_color='rgb(246, 147, 187)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_defi_users'],
                name='# of users',
                marker_color='rgb(115, 61, 7)'
                , yaxis='y2'))

fig3.update_layout(
    title='Polygon DeFi users',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Daily Polygon DeFi users", secondary_y=False)
fig3.update_yaxes(title_text="Total Polygon DeFi users", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily Arbitrum DeFi users", "Daily Optimism DeFi users", "Daily Polygon DeFi users"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)



    
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Line(x=df['date'],
                y=df['avg_tx_per_user'],
                name='# of transactions',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['avg_swaps_per_swapper'],
                name='# of swaps',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['nft_bought_per_user'],
                name='# of nfts',
                marker_color='rgb(55, 55, 55)'
                , yaxis='y2')) 
fig1.add_trace(go.Line(x=df['date'],
                y=df['defi_txs_user'],
                name='# of transactions',
                marker_color='rgb(249, 11, 78)'
                , yaxis='y2'))

fig1.update_layout(
    title='Arbitrum user activity',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily transactions/swaps behavior", secondary_y=False)
fig1.update_yaxes(title_text="Daily NFTs/DeFi behavior", secondary_y=True)


fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Line(x=df2['date'],
                y=df2['avg_tx_per_user'],
                name='# of transactions',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df2['date'],
                y=df2['avg_swaps_per_swapper'],
                name='# of swaps',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df2['date'],
                y=df2['nft_bought_per_user'],
                name='# of nfts',
                marker_color='rgb(55, 55, 55)'
                , yaxis='y2'))
fig2.add_trace(go.Line(x=df2['date'],
                y=df2['defi_txs_user'],
                name='# of transactions',
                marker_color='rgb(249, 11, 78)'
                , yaxis='y2'))

fig2.update_layout(
    title='Optimism user activity',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily transactions/swaps behavior", secondary_y=False)
fig2.update_yaxes(title_text="Daily NFTs/DeFi behavior", secondary_y=True)


fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Line(x=df3['date'],
                y=df3['avg_tx_per_user'],
                name='# of transactions',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df3['date'],
                y=df3['avg_swaps_per_swapper'],
                name='# of swaps',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df3['date'],
                y=df3['nft_bought_per_user'],
                name='# of nfts',
                marker_color='rgb(55, 55, 55)'
                , yaxis='y2'))
fig3.add_trace(go.Line(x=df3['date'],
                y=df3['defi_txs_user'],
                name='# of transactions',
                marker_color='rgb(249, 11, 78)'
                , yaxis='y2'))

fig3.update_layout(
    title='Polygon user activity',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Daily transactions/swaps behavior", secondary_y=False)
fig3.update_yaxes(title_text="Daily NFTs/DeFi behavior", secondary_y=True)


tab1, tab2, tab3 = st.tabs(["Daily Arbitrum user activity", "Daily Optimism user activity", "Daily Polygon user activity"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[ ]:




