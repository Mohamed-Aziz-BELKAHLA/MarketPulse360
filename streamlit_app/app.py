import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text

# ─── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MarketPulse 360",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── DARK THEME CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0B1929; color: #D6E8F5; }
    [data-testid="stSidebar"] { background-color: #0D1F33; border-right: 1px solid #1E3A56; }
    [data-testid="stSidebar"] * { color: #8FB8D8 !important; }
    [data-testid="metric-container"] {
        background: #122237; border: 1px solid #1E3A56;
        border-radius: 10px; padding: 16px;
    }
    [data-testid="metric-container"] label { color: #4A7FA5 !important; font-size: 11px !important; }
    [data-testid="metric-container"] [data-testid="stMetricValue"] { color: #D6E8F5 !important; font-size: 28px !important; }
    h1 { color: #D6E8F5 !important; font-size: 24px !important; }
    h2 { color: #D6E8F5 !important; }
    p, .stMarkdown { color: #8FB8D8; }
    .subtitle { color: #4A7FA5; font-size: 13px; margin-top: -10px; margin-bottom: 20px; }
    .page-label { color: #4A7FA5; font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase; }
    .rec-card {
        background: #122237; border-radius: 10px; padding: 20px;
        border: 1px solid #1E3A56; height: 100%;
    }
    .card-bar { height: 4px; border-radius: 4px; margin-bottom: 14px; }
    .card-category { font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase; margin: 0; }
    .card-metric { font-size: 26px; font-weight: 600; margin: 4px 0 12px 0; }
    .card-label { font-size: 10px; letter-spacing: 0.09em; text-transform: uppercase; color: #3D6080; margin: 8px 0 3px 0; }
    .card-text { font-size: 12px; color: #8FB8D8; line-height: 1.5; margin: 0; }
    .card-action { font-size: 12px; color: #C5DFF2; line-height: 1.5; margin: 0; }
    .card-divider { border: none; border-top: 1px solid #1E3A56; margin: 10px 0; }
    .impact-badge {
        display: inline-block; font-size: 11px; padding: 3px 10px;
        border-radius: 20px; margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ─── DATABASE ─────────────────────────────────────────────────────────────────
@st.cache_resource
def get_engine():
    return create_engine("postgresql://postgres:postgres123@localhost:5432/marketpulse360")

@st.cache_data
def load_data(query):
    return pd.read_sql(query, get_engine())

# ─── PLOTLY TEMPLATE ──────────────────────────────────────────────────────────
LAYOUT = dict(
    paper_bgcolor="#122237",
    plot_bgcolor="#122237",
    font=dict(color="#8FB8D8", size=11),
    legend=dict(bgcolor="#122237", font=dict(color="#8FB8D8")),
    colorway=["#3B82F6","#10B981","#F59E0B","#EF4444","#8B5CF6","#EC4899"],
)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 MarketPulse 360")
    st.markdown("<p style='color:#4A7FA5;font-size:11px;'>Olist E-Commerce · 2016–2018</p>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation", [
        "Executive Overview", "Pricing & Margin", "Customer Segmentation",
        "Risk & Anomaly Control", "Business Recommendations"
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<p style='color:#3D6080;font-size:10px;'>96K orders · 13.28M BRL revenue<br>93K customers · 23K anomalies</p>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "Executive Overview":
    st.markdown("<p class='page-label'>MarketPulse 360 · Olist E-Commerce</p>", unsafe_allow_html=True)
    st.title("Executive Overview")
    st.markdown("<p class='subtitle'>13.28M BRL revenue · 96K orders · 2016–2018</p>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Revenue", "13.28M BRL")
    col2.metric("Total Orders", "96K")
    col3.metric("Avg Order Value", "BRL 137.65")
    col4.metric("Avg Review Score", "4.08 / 5")
    col5.metric("Freight Ratio", "16.64%")

    st.markdown("---")
    col_left, col_right = st.columns([3, 2])

    with col_left:
        try:
            df_rev = load_data("""
                SELECT year, month,
                       SUM(revenue) as total_revenue,
                       COUNT(DISTINCT order_id) as nb_orders
                FROM analytics.mart_revenue
                GROUP BY year, month
                ORDER BY year, month
            """)
            df_rev['period'] = df_rev['year'].astype(str) + '-' + df_rev['month'].astype(str).str.zfill(2)
            fig = go.Figure()
            fig.add_bar(x=df_rev['period'], y=df_rev['total_revenue'],
                       name='Total Revenue', marker_color='#3B82F6', opacity=0.8)
            fig.add_scatter(x=df_rev['period'], y=df_rev['nb_orders'],
                           name='Orders', yaxis='y2',
                           line=dict(color='#10B981', width=2))
            fig.update_layout(
                **LAYOUT,
                title='Monthly Revenue & Orders Trend',
                yaxis=dict(title='Revenue (BRL)', gridcolor='#1E3A56', tickfont=dict(color='#8FB8D8')),
                yaxis2=dict(overlaying='y', side='right', title='Orders',
                           gridcolor='#1E3A56', tickfont=dict(color='#8FB8D8')),
                height=380
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Erreur: {e}")

    with col_right:
        try:
            df_cat = load_data("""
                SELECT p.category,
                       SUM(f.payment_value) as total_revenue
                FROM public.fact_orders f
                JOIN public.dim_products p ON f.product_id = p.product_id
                WHERE p.category IS NOT NULL
                GROUP BY p.category
                ORDER BY total_revenue DESC
                LIMIT 15
            """)
            fig2 = px.bar(df_cat, x='total_revenue', y='category', orientation='h',
                         color_discrete_sequence=['#3B82F6'],
                         labels={'total_revenue': 'Revenue (BRL)', 'category': ''})
            fig2.update_layout(**LAYOUT, title='Revenue by Category', height=380)
            fig2.update_yaxes(categoryorder='total ascending')
            st.plotly_chart(fig2, use_container_width=True)
        except Exception as e:
            st.error(f"Erreur: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PRICING & MARGIN
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Pricing & Margin":
    st.markdown("<p class='page-label'>MarketPulse 360 · Olist E-Commerce</p>", unsafe_allow_html=True)
    st.title("Pricing & Margin Analysis")
    st.markdown("<p class='subtitle'>Price optimization · Freight ratio monitoring</p>", unsafe_allow_html=True)

    try:
        df_price = load_data("""
            SELECT p.category,
                   ROUND(AVG(f.product_price)::numeric, 2) as avg_price,
                   ROUND(AVG(f.freight_value / NULLIF(f.product_price + f.freight_value, 0) * 100)::numeric, 2) as freight_ratio,
                   COUNT(DISTINCT f.order_id) as total_orders
            FROM public.fact_orders f
            JOIN public.dim_products p ON f.product_id = p.product_id
            WHERE p.category IS NOT NULL
            GROUP BY p.category
            ORDER BY freight_ratio DESC
        """)

        col_left, col_right = st.columns([2, 3])

        with col_left:
            st.dataframe(
                df_price.rename(columns={
                    'category': 'Category', 'avg_price': 'Avg Price (BRL)',
                    'freight_ratio': 'Freight Ratio %', 'total_orders': 'Total Orders'
                }),
                use_container_width=True, height=500, hide_index=True
            )

        with col_right:
            fig3 = px.scatter(df_price, x='avg_price', y='freight_ratio',
                             size='total_orders', hover_name='category',
                             color_discrete_sequence=['#3B82F6'],
                             labels={'avg_price': 'Avg Price (BRL)', 'freight_ratio': 'Freight Ratio %'})
            fig3.update_layout(**LAYOUT, title='Price vs Freight Ratio by Category', height=500)
            st.plotly_chart(fig3, use_container_width=True)

    except Exception as e:
        st.error(f"Erreur: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — CUSTOMER SEGMENTATION
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Customer Segmentation":
    st.markdown("<p class='page-label'>MarketPulse 360 · Olist E-Commerce</p>", unsafe_allow_html=True)
    st.title("Customer Segmentation")
    st.markdown("<p class='subtitle'>RFM analysis · 5 segments · 93K customers</p>", unsafe_allow_html=True)

    try:
        df_seg = load_data("""
            SELECT customer_segment as segment,
                   ROUND(AVG(avg_order_value)::numeric, 0) as avg_monetary,
                   COUNT(customer_unique_id) as customers,
                   ROUND(AVG(nb_orders)::numeric, 1) as avg_orders
            FROM analytics.mart_customer_value
            WHERE customer_segment IS NOT NULL
            GROUP BY customer_segment
            ORDER BY avg_monetary DESC
        """)

        COLORS = {
            'Champions': '#10B981', 'Loyal Customers': '#3B82F6',
            'Potential Loyalists': '#8B5CF6', 'At Risk': '#EF4444', 'Lost': '#6B7280'
        }

        col1, col2 = st.columns(2)

        with col1:
            fig4 = px.pie(df_seg, values='customers', names='segment',
                         hole=0.5, color='segment', color_discrete_map=COLORS)
            fig4.update_layout(**LAYOUT, title='Customer Distribution by RFM Segment', height=380)
            st.plotly_chart(fig4, use_container_width=True)

        with col2:
            fig5 = px.bar(df_seg, x='avg_monetary', y='segment', orientation='h',
                         color='segment', color_discrete_map=COLORS,
                         labels={'avg_monetary': 'Avg Order Value (BRL)', 'segment': ''})
            fig5.update_layout(**LAYOUT, title='Avg Spend by Customer Segment',
                              height=380, showlegend=False)
            fig5.update_yaxes(categoryorder='total ascending')
            st.plotly_chart(fig5, use_container_width=True)

        st.dataframe(
            df_seg.rename(columns={
                'segment': 'Segment', 'avg_monetary': 'Avg Order Value (BRL)',
                'customers': 'Customers', 'avg_orders': 'Avg Orders'
            }),
            use_container_width=True, hide_index=True
        )

    except Exception as e:
        st.error(f"Erreur: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — RISK & ANOMALY CONTROL
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Risk & Anomaly Control":
    st.markdown("<p class='page-label'>MarketPulse 360 · Olist E-Commerce</p>", unsafe_allow_html=True)
    st.title("Risk & Anomaly Control")
    st.markdown("<p class='subtitle'>23,765 anomalous transactions detected · 21.4% of orders</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Anomaly Count", "23,765")
    col2.metric("% of Orders", "21.4%")
    col3.metric("Top Risk Category", "furniture_decor")

    st.markdown("---")

    try:
        df_anom = load_data("""
            SELECT p.category,
                   COUNT(f.order_id) as orders,
                   ROUND(AVG(f.product_price)::numeric, 2) as avg_price,
                   ROUND(AVG(f.freight_value)::numeric, 2) as avg_freight,
                   ROUND(AVG(f.freight_value / NULLIF(f.product_price + f.freight_value,0) * 100)::numeric, 1) as freight_ratio_pct
            FROM public.fact_orders f
            JOIN public.dim_products p ON f.product_id = p.product_id
            WHERE p.category IS NOT NULL
            GROUP BY p.category
            ORDER BY orders DESC
            LIMIT 20
        """)

        col_left, col_right = st.columns([2, 3])

        with col_left:
            st.dataframe(
                df_anom.rename(columns={
                    'category': 'Category', 'orders': 'Orders',
                    'avg_price': 'Avg Price', 'avg_freight': 'Avg Freight',
                    'freight_ratio_pct': 'Freight Ratio %'
                }),
                use_container_width=True, height=450, hide_index=True
            )

        with col_right:
            fig6 = px.bar(df_anom, x='orders', y='category', orientation='h',
                         color_discrete_sequence=['#EF4444'],
                         labels={'orders': 'Number of Orders', 'category': ''})
            fig6.update_layout(**LAYOUT, title='Anomalies by Category', height=450)
            fig6.update_yaxes(categoryorder='total ascending')
            st.plotly_chart(fig6, use_container_width=True)

    except Exception as e:
        st.error(f"Erreur: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — BUSINESS RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Business Recommendations":
    st.markdown("<p class='page-label'>MarketPulse 360 · Olist E-Commerce</p>", unsafe_allow_html=True)
    st.title("Business Recommendations")
    st.markdown("<p class='subtitle'>Data-driven actions · 4 strategic initiatives identified</p>", unsafe_allow_html=True)

    def rec_card(color, cat_color, category, metric, metric_color, finding, action, badge_text, badge_color):
        return f"""
        <div class="rec-card">
            <div class="card-bar" style="background:{color};"></div>
            <p class="card-category" style="color:{cat_color};">{category}</p>
            <p class="card-metric" style="color:{metric_color};">{metric}</p>
            <hr class="card-divider">
            <p class="card-label">Finding</p>
            <p class="card-text">{finding}</p>
            <p class="card-label">Action</p>
            <p class="card-action">{action}</p>
            <div><span class="impact-badge" style="background:{badge_color}22;color:{badge_color};border:1px solid {badge_color}44;">{badge_text}</span></div>
        </div>"""

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(rec_card(
            "#F59E0B", "#B07A0A", "PRICING & MARGIN", "+BRL 150K", "#FCD34D",
            "bed_bath_table carries a 19.7% freight ratio across 9,272 orders — highest cost leakage in the catalog.",
            "Negotiate logistics contracts or reprice by +8% to recover margin.",
            "+BRL 150,000 / year", "#F59E0B"
        ), unsafe_allow_html=True)

    with col2:
        st.markdown(rec_card(
            "#3B82F6", "#1D4A8A", "CUSTOMER RETENTION", "13,436", "#93C5FD",
            "73% of customers purchased only once. At Risk segment inactive for an avg. 364 days.",
            "Launch re-engagement campaign with 15% discount targeting 13,436 At Risk customers.",
            "13,436 customers at risk", "#3B82F6"
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        st.markdown(rec_card(
            "#EF4444", "#8A1D1D", "RISK & ANOMALY CONTROL", "23,765", "#FCA5A5",
            "21.4% of all transactions flagged as anomalous. Concentrated in furniture_decor and bed_bath_table.",
            "Deploy automated payment reconciliation checks; prioritize the two highest-risk categories.",
            "21.4% of orders · Critical", "#EF4444"
        ), unsafe_allow_html=True)

    with col4:
        st.markdown(rec_card(
            "#10B981", "#0A5C3A", "GROWTH OPPORTUNITY", "BRL 245", "#6EE7B7",
            "Champions segment (15,115 customers) generates BRL 245 avg/order — 3.4× above base segment.",
            "Launch a VIP loyalty program to increase Champions' purchase frequency and reduce churn.",
            "15,115 VIP customers", "#10B981"
        ), unsafe_allow_html=True)