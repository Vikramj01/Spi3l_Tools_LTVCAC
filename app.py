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
    **Brought to you by [Spi3L LLC](https://spi3l.com)** | 
    [Find us on LinkedIn](https://www.linkedin.com/company/spi3l/?viewAsMember=true)
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
        
        # LTV Input fields with sliders for percentages
        saas_arpa = st.number_input(
            "Average Revenue Per Account (ARPA) - Monthly ($)", 
            min_value=0.0, 
            value=250.0, 
            step=10.0,
            help="The average amount of money you get from one customer each month. (Total Monthly Recurring Revenue / Total Customers)."
        )
        saas_gross_margin = st.slider(
            "Gross Margin (%)", 
            min_value=0.0, 
            max_value=100.0, 
            value=80.0, 
            step=0.1,
            format="%.1f%%",
            help="The percentage of revenue left after paying for the 'cost of goods sold' (COGS). For SaaS, this is often hosting, support, and third-party API costs."
        )
        saas_churn_rate = st.slider(
            "Customer Churn Rate (%) - Monthly", 
            min_value=0.0, 
            max_value=100.0, 
            value=5.0, 
            step=0.1,
            format="%.1f%%",
            help="The percentage of customers who cancel their subscription each month. (Customers who canceled this month / Total customers at start of month)."
        )

        # LTV Calculation for SaaS
        if saas_churn_rate > 0:
            customer_lifetime_months = 1 / (saas_churn_rate / 100)
            saas_ltv = saas_arpa * (saas_gross_margin / 100) * customer_lifetime_months
        else:
            customer_lifetime_months = float('inf') # Or a large number to represent very low churn
            saas_ltv = 0 # Handle gracefully if churn is zero

    with cac_col:
        st.subheader("Customer Acquisition Cost (CAC) Inputs")
        
        # CAC Input fields
        saas_spend = st.number_input(
            "Total Sales & Marketing Spend (Monthly, $)", 
            min_value=0, 
            value=10000, 
            step=500,
            help="The total cost for one month, including salaries, ad spend, software tools, etc."
        )
        saas_new_customers = st.number_input(
            "New Customers Acquired (Monthly)", 
            min_value=0, 
            value=20, 
            step=1,
            help="The total number of new customers you won in that same period."
        )
        
        # CAC Calculation for SaaS
        saas_cac = saas_spend / saas_new_customers if saas_new_customers > 0 else 0

    st.divider()

    # --- Results Section for SaaS ---
    st.subheader("📊 Results")

    if saas_cac > 0:
        saas_ratio = saas_ltv / saas_cac
        
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("Lifetime Value (LTV)", f"${saas_ltv:,.2f}")
        res_col2.metric("Customer Acquisition Cost (CAC)", f"${saas_cac:,.2f}")
        res_col3.metric("LTV:CAC Ratio", f"{saas_ratio:,.2f} : 1")
        
        # Dynamic Feedback
        if saas_ratio >= 3:
            st.success("✅ **Healthy.** Your business model appears sustainable and profitable. Great job!", icon="🎉")
        elif saas_ratio >= 1:
            st.warning("⚠️ **Needs Improvement.** Your business is viable, but there's room to improve profitability by increasing LTV or decreasing CAC.", icon="📈")
        else:
            st.error("🚨 **Unsustainable.** You are spending more to acquire a customer than they are worth. Immediate action is needed to fix your business model.", icon="🔥")
        
        # Bar Chart Visualization
        st.write("---")
        st.subheader("Visual Comparison")
        chart_data = pd.DataFrame({
            'Metric': ['Lifetime Value (LTV)', 'Customer Acquisition Cost (CAC)'],
            'Value ($)': [saas_ltv, saas_cac]
        })
        st.bar_chart(chart_data.set_index('Metric'))

    else:
        st.warning("Please enter a non-zero value for New Customers Acquired to calculate the results.")


# --- Professional Services Model Tab ---
with services_tab:
    st.header("Professional Services / Agency Model Calculator")
    st.info("💡 **Showing example data.** Please replace the values below with your own business's numbers to get an accurate calculation.", icon="ℹ️")

    ltv_col, cac_col = st.columns(2, gap="large")

    with ltv_col:
        st.subheader("Lifetime Value (LTV) Inputs")
        
        serv_annual_value = st.number_input(
            "Average Annual Client Value ($)", 
            min_value=0.0, 
            value=50000.0, 
            step=1000.0,
            help="The average amount a single client pays you over a 12-month period. (Total Annual Revenue / Number of Clients)."
        )
        serv_gross_margin = st.slider(
            "Gross Margin (%)", 
            min_value=0.0, 
            max_value=100.0, 
            value=40.0, 
            step=0.1,
            format="%.1f%%",
            help="The percentage of revenue left after paying for the 'cost of service delivery,' which includes your team's salaries for billable work."
        )
        serv_lifespan = st.number_input(
            "Average Client Lifespan (Years)", 
            min_value=0.0, 
            value=3.0, 
            step=0.5,
            help="The average number of years a client stays with your firm. A good starting point is often 2-3 years."
        )

        # LTV Calculation for Services
        serv_ltv = serv_annual_value * (serv_gross_margin / 100) * serv_lifespan

    with cac_col:
        st.subheader("Customer Acquisition Cost (CAC) Inputs")
        
        serv_spend = st.number_input(
            "Total Sales & Marketing Spend (Quarterly, $)", 
            min_value=0, 
            value=30000, 
            step=500,
            key="serv_spend", # Unique key to avoid widget duplication error
            help="The total cost for a period (e.g., a quarter), including salaries, ad spend, software tools, etc."
        )
        serv_new_customers = st.number_input(
            "New Clients Acquired (Quarterly)", 
            min_value=0, 
            value=5, 
            step=1,
            key="serv_new_customers",
            help="The total number of new clients you won in that same period."
        )
        
        # CAC Calculation for Services
        serv_cac = serv_spend / serv_new_customers if serv_new_customers > 0 else 0

    st.divider()

    # --- Results Section for Services ---
    st.subheader("📊 Results")
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

        # Bar Chart Visualization
        st.write("---")
        st.subheader("Visual Comparison")
        chart_data = pd.DataFrame({
            'Metric': ['Lifetime Value (LTV)', 'Customer Acquisition Cost (CAC)'],
            'Value ($)': [serv_ltv, serv_cac]
        })
        st.bar_chart(chart_data.set_index('Metric'))
    else:
        st.warning("Please enter a non-zero value for New Clients Acquired to calculate the results.")

# --- High-Value / One-Off Sale Model Tab ---
with one_off_tab:
    st.header("High-Value / One-Off Sale Model Calculator")
    st.info("💡 **Showing example data.** Please replace the values below with your own business's numbers to get an accurate calculation.", icon="ℹ️")

    ltv_col, cac_col = st.columns(2, gap="large")

    with ltv_col:
        st.subheader("Lifetime Value (LTV) Inputs")

        one_off_margin_value = st.number_input(
            "Gross Margin on Initial Sale ($)",
            min_value=0.0,
            value=500000.0,
            step=1000.0,
            help="The total profit (in dollars) from the primary sale. (Sale Price - Cost of Goods Sold)."
        )
        one_off_service_revenue = st.number_input(
            "Expected Annual Service Revenue ($)",
            min_value=0.0,
            value=25000.0,
            step=500.0,
            help="The average revenue you expect from service contracts or spare parts per year."
        )
        one_off_service_margin = st.slider(
            "Gross Margin on Service Revenue (%)",
            min_value=0.0,
            max_value=100.0,
            value=60.0,
            step=0.1,
            format="%.1f%%",
            help="The profit margin on your service and parts business, which is often high."
        )
        one_off_service_lifespan = st.number_input(
            "Expected Lifespan of Service (Years)",
            min_value=0.0,
            value=5.0,
            step=0.5,
            help="How many years you expect to retain the service contract."
        )
        
        # LTV Calculation for One-Off
        lifetime_service_value = one_off_service_revenue * (one_off_service_margin / 100) * one_off_service_lifespan
        one_off_ltv = one_off_margin_value + lifetime_service_value

    with cac_col:
        st.subheader("Customer Acquisition Cost (CAC) Inputs")
        
        one_off_spend = st.number_input(
            "Total Sales & Marketing Spend (Annually, $)",
            min_value=0,
            value=200000,
            step=1000,
            key="one_off_spend",
            help="The total cost for a long sales cycle (e.g., a year), including salaries, travel, trade shows, etc."
        )
        one_off_new_customers = st.number_input(
            "New Customers Acquired (Annually)",
            min_value=0,
            value=2,
            step=1,
            key="one_off_new_customers",
            help="The total number of new customers you won in that same period."
        )
        
        # CAC Calculation for One-Off
        one_off_cac = one_off_spend / one_off_new_customers if one_off_new_customers > 0 else 0

    st.divider()

    # --- Results Section for One-Off ---
    st.subheader("📊 Results")
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
        
        # Bar Chart Visualization
        st.write("---")
        st.subheader("Visual Comparison")
        chart_data = pd.DataFrame({
            'Metric': ['Lifetime Value (LTV)', 'Customer Acquisition Cost (CAC)'],
            'Value ($)': [one_off_ltv, one_off_cac]
        })
        st.bar_chart(chart_data.set_index('Metric'))
    else:
        st.warning("Please enter a non-zero value for New Customers Acquired to calculate the results.")