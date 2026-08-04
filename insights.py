import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

# Load the data
bls_df = pd.read_csv('Brand Lift Study Results - Sheet1.csv')
historic_df = pd.read_csv('Historic Campaign Data - Sheet1.csv')

#Create 'is_significant' column
def check_significance(row):
    # Successes: [Exposed, Control], Totals: [Exposed, Control]
    counts = [row['Exposed_Consideration'], row['Control_Consideration']]
    sample_size = [row['Exposed_Responses'], row['Control_Responses']]

    # Calculate p-value for this specific row
    stat, pval = proportions_ztest(counts, sample_size)

    # Check results
    if pval < 0.05:
        print("Statistically Significant")
        return True
    else:
        print("Not Significant")
        return False
    #return pval < 0.05  # Returns True if significant, False if not

# Apply the function to create the column you were missing
bls_df['is_significant'] = bls_df.apply(check_significance, axis=1)

#Merge the data (merge historic campaign data with brand life study data)
join_columns = ['Campaign_Name', 'Market', 'Channel']

# We bring over the rates and the created significance column
payload_columns = ['Exposed_Rate', 'Control_Rate', 'is_significant', 'Relative_Lift']

#join the selected data (payload_columns) from brand lift study with the historic campaign data
result = historic_df.merge(
    bls_df[join_columns + payload_columns],
    on=join_columns,
    how='left'
)

#Efficiency Calculations

# 1. Absolute Lift %
result['abs_lift_pct'] = result['Exposed_Rate'] - result['Control_Rate']

# 2. Volume of Lifted Users (Reach * Lift %)
result['lifted_users'] = result['Reach'] * result['abs_lift_pct']

# 3. Cost Per Lifted User (Spend / Lifted Users)
# Using .mask to handle cases where lifted_users is 0 or negative
result['cost_per_lifted_user'] = result['Spend_USD'] / result['lifted_users'].mask(result['lifted_users'] <= 0)

# 4. Filter for only Statistically Significant impact
significant_results = result[result['is_significant'] == True].copy()

# 5. Sort by Efficiency (Lower cost = better)
significant_results = significant_results.sort_values('cost_per_lifted_user', ascending=True)

# --- STEP 4: See your results ---
print("Top 5 Most Efficient Campaigns:")
print(significant_results[['Campaign_Name', 'Market', 'Channel', 'cost_per_lifted_user']].head())

#--------------------------Effective and statistically Significant Campaigns----------------------------------------------

# 1. Find the statistically significant campaign
significant_campaigns = result[result['is_significant'] == True].copy()

# 2. Sort by Relative_Lift in descending order (Highest at the top)
effective_campaigns = significant_campaigns.sort_values('Relative_Lift', ascending=False)

effective_campaigns_list = effective_campaigns[['Campaign_Name', 'Market', 'Channel', 'Relative_Lift']]

# 3. Print out the table
print("--- Most Effective and Statistically Significant campaigns (Highest Relative Lift) ---")
print(effective_campaigns_list)

#----------------------Best Performance market/channel------------------------------------
# 1. Group the data by Market and Channel
# We sum the Spend and Lifted Users to see the total impact per group
summary = result.groupby(['Market', 'Channel']).agg({
    'Spend_USD': 'sum',
    'lifted_users': 'sum'
}).reset_index()

# 2. Calculate the "True" Efficiency for the group
# (Total Spend in that group / Total Users influenced in that group)
summary['CPLU'] = summary['Spend_USD'] / summary['lifted_users']

# 3. Sort by Efficiency (Lower CPLU is better)
summary = summary.sort_values('CPLU', ascending=True)

print("--- Performance Summary by Market & Channel ---")
print(summary)

#-----------------------------Relative Cost-------------------------------------
# 1. Group by Market and Channel to get total Spend and total Reach
targeting_costs = result.groupby(['Market', 'Channel']).agg({
    'Spend_USD': 'sum',
    'Reach': 'sum'
}).reset_index()

# 2. Calculate Cost Per Reach (CPR)
targeting_costs['CPR'] = targeting_costs['Spend_USD'] / targeting_costs['Reach']

# 3. Calculate Global Average CPR to use as a baseline
avg_cpr = targeting_costs['CPR'].mean()

# 4. Calculate the Relative Cost Index
# 100 is average. 120 means it's 20% more expensive than average. 80 means it's 20% cheaper.
targeting_costs['Relative_Cost_Index'] = (targeting_costs['CPR'] / avg_cpr) * 100

# 5. Sort by most expensive to target
targeting_costs = targeting_costs.sort_values('Relative_Cost_Index', ascending=False)

print("--- Relative Cost to Target by Market/Channel ---")
print(targeting_costs[['Market', 'Channel', 'CPR', 'Relative_Cost_Index']])

#-------------------------- Creative Resonance --------------------------

creative_df = pd.read_csv('Creative Performance Report - Sheet1.csv')

# 1. Which Creative resonated best globally?
# We average the Consideration lift across all age groups and markets
best_creative = creative_df.groupby('Creative_Name')['Point_Est_Consideration'].mean().sort_values(ascending=False)

# 2. Does this differ by Market?
# We look at the average performance of each creative within each market
market_resonance = creative_df.groupby(['Market', 'Creative_Name'])['Point_Est_Consideration'].mean().unstack()

# 3. Which Channel was best for resonance?
channel_resonance = creative_df.groupby('Channel')['Point_Est_Consideration'].mean().sort_values(ascending=False)

print("--- Global Creative Resonance (Avg Consideration Lift) ---")
print(best_creative)

print("\n--- Resonance by Market ---")
print(market_resonance)

print("\n--- Resonance by Channel ---")
print(channel_resonance)