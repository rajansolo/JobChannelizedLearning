import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_json('StudentData.json')
print(len(data))
result = []
context={}
job_count_string=''

for index, row in data.iterrows():
  name = row['Name']
  company = row['Company']
  role = row['Role']
  date = row['Date']
  internshipDuration= row['InternshipDuration']
  intake = row['Intake']

  data_ap = {
      'name': name,
      'company': company,
      'role': role,
      'date': date,
      'internshipDuration': internshipDuration,
      'intake': intake,
  }
  result.append(data_ap)

print(result)

# Create a dictionary to store the counts of each role
role_counts = {}

# Loop through the data and count the roles
for item in result:
    role = item['role']
    if role in role_counts:
        role_counts[role] += 1
    else:
        role_counts[role] = 1

# Sort the roles by count in descending order and print the top 10
sorted_roles = sorted(role_counts.items(), key=lambda x: x[1], reverse=True)
for i, (role, count) in enumerate(sorted_roles[:10]):
    print(f'{i + 1}. {role}: {count}')
    job_count_string = job_count_string +'\n '+ str(f'{i + 1}. {role}: {count}')
context['result'] = job_count_string

# Extract the role names and counts for the bar chart
roles = [role for role, count in sorted_roles[:10]]
counts = [count for role, count in sorted_roles[:10]]

# Create a bar chart of the top 10 roles
plt.bar(roles, counts)
plt.title('Top 10 Roles')
plt.xlabel('Role')
plt.ylabel('Count')
plt.show()

# Count the number of roles for each company
company_counts = {}
for item in result:
    company = item['company']
    if company in company_counts:
        company_counts[company] += 1
    else:
        company_counts[company] = 1

# Sort the companies by number of Students
sorted_companies = sorted(company_counts.items(), key=lambda x: x[1], reverse=True)

job_count_string=''
# Print the top 5 companies by number of Students
print("Top 5 companies by number of Students:")
for company, count in sorted_companies[:5]:
    print(f"{company}: {count} Students")
    job_count_string = job_count_string+ '\n '+ str(f"{company}: {count} Students")

context['result'] = context['result'] + job_count_string
#Creating chart for the top companies
# Create the bar chart
fig, ax = plt.subplots()
ax.barh(range(len(sorted_companies)), [count for company, count in sorted_companies], align='center')
ax.set_yticks(range(len(sorted_companies)))
ax.set_yticklabels([company for company, count in sorted_companies])
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Number of Students')
ax.set_title('Number of Students per company')

plt.show()

# Sort the data by company and role
result.sort(key=lambda x: (x['company'], x['role']))

# Initialize a dictionary to store the role counts for each company
company_role_counts = {}

# Loop through the data and count the roles for each company
current_company = None
current_role_counts = {}
for item in result:
    company = item['company']
    role = item['role']
    if company != current_company:
        if current_company is not None:
            company_role_counts[current_company] = current_role_counts
        current_company = company
        current_role_counts = {}
    if role in current_role_counts:
        current_role_counts[role] += 1
    else:
        current_role_counts[role] = 1

# Add the role counts for the last company to the dictionary
company_role_counts[current_company] = current_role_counts

job_count_string=''
# Print the results
print()
for company, role_counts in company_role_counts.items():
    print(f"{company}:")
    job_count_string=job_count_string+'\n '+ str(f"{company}:")
    for role, count in role_counts.items():
        job_count_string=job_count_string+'\n '+str(f"- {role}: {count}")
        print(f"- {role}: {count}")
    print()

context['result'] = context['result'] + job_count_string


#####################################chart1####################################


# Sort the data by company and role
result.sort(key=lambda x: (x['company'], x['role']))

# Initialize a dictionary to store the role counts for each company
company_role_counts = {}

# Loop through the data and count the roles for each company
current_company = None
current_role_counts = {}
for item in result:
    company = item['company']
    role = item['role']
    if company != current_company:
        if current_company is not None:
            company_role_counts[current_company] = current_role_counts
        current_company = company
        current_role_counts = {}
    if role in current_role_counts:
        current_role_counts[role] += 1
    else:
        current_role_counts[role] = 1

# Add the role counts for the last company to the dictionary
company_role_counts[current_company] = current_role_counts

# Create a list of unique roles
all_roles = set()
for role_counts in company_role_counts.values():
    all_roles.update(role_counts.keys())

# Sort the roles by total count
role_counts = {}
for role in all_roles:
    role_count = sum(counts.get(role, 0) for counts in company_role_counts.values())
    role_counts[role] = role_count
sorted_roles = sorted(role_counts.items(), key=lambda x: x[1], reverse=True)

# Get the top 10 roles
top_roles = sorted_roles[:10]
top_role_names = [role for role, count in top_roles]

# Create a list of companies and a list of the role counts for each company
companies = list(company_role_counts.keys())
role_counts_by_company = []
for company, role_counts in company_role_counts.items():
    role_counts_for_company = [role_counts.get(role, 0) for role in top_role_names]
    role_counts_by_company.append(role_counts_for_company)


#Creating scatter plot
# Convert the dictionary of role counts to a DataFrame
df = pd.DataFrame.from_dict(company_role_counts, orient='index')

# Reset the index to make the company column a regular column
df = df.reset_index().rename(columns={'index': 'company'})

# Convert the DataFrame to long form
df_long = df.melt(id_vars=['company'], var_name='role', value_name='count')

# Create a scatter plot with company on the x-axis, role on the y-axis, and count as the size of the markers
plt.scatter(df_long['company'], df_long['role'], s=df_long['count']*10)
plt.xticks(rotation=90)
plt.xlabel('Company')
plt.ylabel('Role')
plt.title('Role Counts by Company')
plt.show()
print(context)