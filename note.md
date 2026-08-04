print(f"{'Campaign_Name'} | {'Market':<10} | {'Channel':<10} | {'P-Value':<12} | {'Significant?'}")
print("-" * 55)

# 2. Iterate through each row of the CSV
for index, row in df.iterrows():
    # Pull values for the current row
    counts = [row['Exposed_Consideration'], row['Control_Consideration']]
    nobs = [row['Exposed_Responses'], row['Control_Responses']]

    # 3. Calculate p-value for this specific row
    stat, pval = proportions_ztest(counts, nobs)

    # 4. Determine if it's significant (using 0.05 threshold)
    is_significant = "YES" if pval < 0.05 else "No"

    # 5. Print the result for this row
    campaign_name = row['Campaign_Name']
    market = row['Market']
    channel = row['Channel']
    print(f"{campaign_name} | {market:<10} | {channel:<10} | {pval:<12.4e} | {is_significant}")