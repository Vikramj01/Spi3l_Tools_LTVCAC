import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="B2B Growth Engine Calculator",
    page_icon="🚀",
    layout="wide"
)

# --- Main Application ---

# --- Title and Introduction ---
# Create two columns for the header
logo_col, title_col = st.columns([1, 4]) # The numbers represent the width ratio

with logo_col:
    # --- IMPORTANT ---
    # Replace 'logo.png' with the actual path to your logo image file.
    st.image("logo.png", width=150) 

with title_col:
    st.title("🚀 The B2B Growth Engine Calculator")
    
    # --- IMPORTANT ---
    # Replace the URLs with your actual website and social media links.
    st.markdown("""
    **Brought to you by [Your Company Name](https://yourwebsite.com)** | 
    [Read the Full Article](https://yourwebsite.com/blog) | 
    [Find us on LinkedIn](https://www.linkedin.com/company/your-company)
    """)

st.markdown("""
Welcome to the LTV:CAC Business Health Calculator. This tool is designed to help you understand the core economics of your business. 
The **Lifetime Value (LTV) to Customer Acquisition Cost (CAC) ratio** is a critical metric that measures the long-term value of a customer against the cost of acquiring them. 
A healthy ratio (typically 3:1 or higher) indicates a sustainable and profitable business model. 

Use the tabs below to select the model that best fits your business and find your ratio.
""")

# --- Tabbed Navigation ---
saas_tab, services_tab, one_off_tab = st.tabs([
    "📈 SaaS / Subscription", 
    "👥 Professional Services / Agency", 
    "🏭 High-Value / One-Off Sale"
])


# --- SaaS / Subscription Model Tab ---
with saas_tab:
    st.header("SaaS / Subscription Model Calculator")
    st.info("💡 **Showing example data.** Please replace the values below with your own business's numbers to get an accurate calculation.", icon="ℹ️")
    
    # Create columns for layout
    ltv_col, cac_col = st.columns(2, gap="large")

    with ltv_col:
        st.subheader("Lifetime Value (LTV) Inputs")
        
        saas_arpa = st.number_input("Average Revenue Per Account (ARPA) - Monthly ($)", min_value=0.0, value=250.0, step=10.0, help="...")
        saas_gross_margin = st.slider("Gross Margin (%)", 0.0, 100.0, 80.0, 0.1, format="%.1f%%", help="...")
        saas_churn_rate = st.slider("Customer Churn Rate (%) - Monthly", 0.0, 100.0, 5.0, 0.1, format="%.1f%%", help="...")

        if saas_churn_rate > 0:
            customer_lifetime_months = 1 / (saas_churn_rate / 100)
            saas_ltv = saas_arpa * (saas_gross_margin / 100) * customer_lifetime_months
        else:
            customer_lifetime_months = float('inf')
            saas_ltv = 0

    with cac_col:
        st.subheader("Customer Acquisition Cost (CAC) Inputs")
        
        saas_spend = st.number_input("Total Sales & Marketing Spend (Monthly, $)", min_value=0, value=10000, step=500, help="...")
        saas_new_customers = st.number_input("New Customers Acquired (Monthly)", min_value=0, value=20, step=1, help="...")
        
        saas_cac = saas_spend / saas_new_customers if saas_new_customers > 0 else 0

    st.divider()

    st.subheader("📊 Snapshot Results")
    if saas_cac > 0:
        saas_ratio = saas_ltv / saas_cac
        
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("Lifetime Value (LTV)", f"${saas_ltv:,.2f}")
        res_col2.metric("Customer Acquisition Cost (CAC)", f"${saas_cac:,.2f}")
        res_col3.metric("LTV:CAC Ratio", f"{saas_ratio:,.2f} : 1")
        
        if saas_ratio >= 3:
            st.success("✅ **Healthy.** Your business model appears sustainable and profitable. Great job!", icon="🎉")
        elif saas_ratio >= 1:
            st.warning("⚠️ **Needs Improvement.** Your business is viable, but there's room to improve profitability by increasing LTV or decreasing CAC.", icon="📈")
        else:
            st.error("🚨 **Unsustainable.** You are spending more to acquire a customer than they are worth. Immediate action is needed to fix your business model.", icon="🔥")
        
        st.write("---")
        st.subheader("Visual Comparison")
        chart_data = pd.DataFrame({'Metric': ['Lifetime Value (LTV)', 'Customer Acquisition Cost (CAC)'], 'Value ($)': [saas_ltv, saas_cac]})
        st.bar_chart(chart_data.set_index('Metric'))
    else:
        st.warning("Please enter a non-zero value for New Customers Acquired to calculate the snapshot results.")

    # --- NEW: TREND ANALYSIS SECTION ---
    st.divider()
    st.subheader("📈 LTV:CAC Trend Analysis")
    st.markdown("Analyze how your acquisition efficiency has changed over time. Your calculated LTV above will be used to calculate the ratio for each period.")
    
    if saas_ltv > 0:
        # Create an editable dataframe for user input
        trend_data = {
            'Period': ['January', 'February', 'March', 'April', 'May', 'June'],
            'Total Sales & Marketing Spend ($)': [9000, 9500, 10000, 11000, 10500, 11500],
            'New Customers Acquired': [18, 19, 20, 21, 22, 21]
        }
        trend_df = pd.DataFrame(trend_data)
        
        st.write("**Enter your historical data for each period below:**")
        edited_df = st.data_editor(trend_df, num_rows="dynamic")

        # Perform calculations on the edited dataframe
        edited_df['CAC ($)'] = edited_df['Total Sales & Marketing Spend ($)'] / edited_df['New Customers Acquired']
        edited_df['LTV:CAC Ratio'] = saas_ltv / edited_df['CAC ($)']
        
        st.write("**Trend Results:**")
        
        # Display the line chart
        st.line_chart(edited_df.set_index('Period')['LTV:CAC Ratio'])
        
        # Display the data table as well
        with st.expander("Show Trend Data Table"):
            st.dataframe(edited_df)
    else:
        st.warning("Please calculate a valid LTV in the section above to enable the trend analysis.")
        
# --- Professional Services Model Tab ---
# (Code for this tab remains unchanged for now)
with services_tab:
    st.header("Professional Services / Agency Model Calculator")
    st.info("💡 **Showing example data.** Please replace the values below with your own business's numbers to get an accurate calculation.", icon="ℹ️")
    # ... (rest of the code for this tab is the same)
    ltv_col, cac_col = st.columns(2, gap="large")
    with ltv_col:
        st.subheader("Lifetime Value (LTV) Inputs")
        serv_annual_value = st.number_input("Average Annual Client Value ($)", min_value=0.0, value=50000.0, step=1000.0, help="...")
        serv_gross_margin = st.slider("Gross Margin (%)", 0.0, 100.0, 40.0, 0.1, format="%.1f%%", key="serv_gm", help="...")
        serv_lifespan = st.number_input("Average Client Lifespan (Years)", min_value=0.0, value=3.0, step=0.5, help="...")
        serv_ltv = serv_annual_value * (serv_gross_margin / 100) * serv_lifespan
    with cac_col:
        st.subheader("Customer Acquisition Cost (CAC) Inputs")
        serv_spend = st.number_input("Total Sales & Marketing Spend (Quarterly, $)", min_value=0, value=30000, step=500, key="serv_spend", help="...")
        serv_new_customers = st.number_input("New Clients Acquired (Quarterly)", min_value=0, value=5, step=1, key="serv_new_customers", help="...")
        serv_cac = serv_spend / serv_new_customers if serv_new_customers > 0 else 0
    st.divider()
    st.subheader("📊 Snapshot Results")
    if serv_cac > 0:
        serv_ratio = serv_ltv / serv_cac
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("Lifetime Value (LTV)", f"${serv_ltv:,.2f}")
        res_col2.metric("Customer Acquisition Cost (CAC)", f"${serv_cac:,.2f}")
        res_col3.metric("LTV:CAC Ratio", f"{serv_ratio:,.2f} : 1")
        if serv_ratio >= 3:
            st.success("✅ **Healthy.** Your business model appears sustainable and profitable. Great job!", icon="🎉")
        elif serv_ratio >= 1:
            st.warning("⚠️ **Needs Improvement.** Your business is viable, but there's room to improve profitability by increasing LTV or decreasing CAC.", icon="📈")
        else:
            st.error("🚨 **Unsustainable.** You are spending more to acquire a client than they are worth. Immediate action is needed to fix your business model.", icon="🔥")
        st.write("---")
        st.subheader("Visual Comparison")
        chart_data_serv = pd.DataFrame({'Metric': ['Lifetime Value (LTV)', 'Customer Acquisition Cost (CAC)'], 'Value ($)': [serv_ltv, serv_cac]})
        st.bar_chart(chart_data_serv.set_index('Metric'))
    else:
        st.warning("Please enter a non-zero value for New Clients Acquired to calculate the snapshot results.")

# --- High-Value / One-Off Sale Model Tab ---
# (Code for this tab remains unchanged for now)
with one_off_tab:
    st.header("High-Value / One-Off Sale Model Calculator")
    st.info("💡 **Showing example data.** Please replace the values below with your own business's numbers to get an accurate calculation.", icon="ℹ️")
    # ... (rest of the code for this tab is the same)
    ltv_col, cac_col = st.columns(2, gap="large")
    with ltv_col:
        st.subheader("Lifetime Value (LTV) Inputs")
        one_off_margin_value = st.number_input("Gross Margin on Initial Sale ($)", min_value=0.0, value=500000.0, step=1000.0, help="...")
        one_off_service_revenue = st.number_input("Expected Annual Service Revenue ($)", min_value=0.0, value=25000.0, step=500.0, help="...")
        one_off_service_margin = st.slider("Gross Margin on Service Revenue (%)", 0.0, 100.0, 60.0, 0.1, format="%.1f%%", help="...")
        one_off_service_lifespan = st.number_input("Expected Lifespan of Service (Years)", min_value=0.0, value=5.0, step=0.5, help="...")
        lifetime_service_value = one_off_service_revenue * (one_off_service_margin / 100) * one_off_service_lifespan
        one_off_ltv = one_off_margin_value + lifetime_service_value
    with cac_col:
        st.subheader("Customer Acquisition Cost (CAC) Inputs")
        one_off_spend = st.number_input("Total Sales & Marketing Spend (Annually, $)", min_value=0, value=200000, step=1000, key="one_off_spend", help="...")
        one_off_new_customers = st.number_input("New Customers Acquired (Annually)", min_value=0, value=2, step=1, key="one_off_new_customers", help="...")
        one_off_cac = one_off_spend / one_off_new_customers if one_off_new_customers > 0 else 0
    st.divider()
    st.subheader("📊 Snapshot Results")
    if one_off_cac > 0:
        one_off_ratio = one_off_ltv / one_off_cac
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("Total Lifetime Value (LTV)", f"${one_off_ltv:,.2f}")
        res_col2.metric("Customer Acquisition Cost (CAC)", f"${one_off_cac:,.2f}")
        res_col3.metric("LTV:CAC Ratio", f"{one_off_ratio:,.2f} : 1")
        if one_off_ratio >= 3:
            st.success("✅ **Healthy.** Your business model appears sustainable and profitable. Great job!", icon="🎉")
        elif one_off_ratio >= 1:
            st.warning("⚠️ **Needs Improvement.** Your business is viable, but there's room to improve profitability by increasing LTV or decreasing CAC.", icon="📈")
        else:
            st.error("🚨 **Unsustainable.** You are spending more to acquire a customer than they are worth. Immediate action is needed to fix your business model.", icon="🔥")
        st.write("---")
        st.subheader("Visual Comparison")
        chart_data_one_off = pd.DataFrame({'Metric': ['Lifetime Value (LTV)', 'Customer Acquisition Cost (CAC)'], 'Value ($)': [one_off_ltv, one_off_cac]})
        st.bar_chart(chart_data_one_off.set_index('Metric'))
    else:
        st.warning("Please enter a non-zero value for New Customers Acquired to calculate the snapshot results.")