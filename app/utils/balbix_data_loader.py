import pandas as pd
import ast
import zipfile
from io import BytesIO

# Generic functions
# Function to convert string lists to actual lists (for tags, roles)
def convert_string_to_list(string):
    try:
        return ast.literal_eval(string)
    except ValueError:
        return []
    except SyntaxError:
        return []

# Function to convert string lists of dictionaries into actual Python objects (for network data)
def convert_str_to_objects(string):
    try:
        return ast.literal_eval(string)
    except Exception as e:
        print(f"Error converting string: {e}")
        return None

def is_empty_list(x):
    return x == []

# # # # # # # # # # # # # # #
# Asset File Loaders
# # # # # # # # # # # # # # #

# The import spec ensures proper handling of data types while the file is being read; important for large datasets
asset_file_import_spec = {
    'NAME': 'string',
    'IMPACT': 'object',
    'LIKELIHOOD': 'object',
    'RISK': 'object',
    'MAC Addresses': 'string',
    'IP Addresses': 'string',
    'SERIAL NUMBER': 'string',
    'GEO LOCATION': 'object',
    'ASSET TYPE': 'object',
    'ASSET SUBTYPE': 'object',
    'OPERATING SYSTEM': 'object',
    'OS PATCH STATUS': 'object',
    'LAST PATCH DATE': 'object',
    'MANUFACTURER': 'object',
    'SITE': 'object',
    'LAST OBSERVED': 'object',
    'FIRST OBSERVED': 'object',
    'LAST PROCESSED': 'object',
    'Roles': 'object',
    'Ports': 'object',
    'TAGS': 'object',
    'Interface Info (IP,MAC,SUBNET,VLAN)': 'object',
    'ACTIVE ISSUES': 'object',
    'CVEs': 'object',
    'REBOOT PENDING STATUS': 'object',
    'UPTIME IN DAYS': 'object',
    'OBSERVERS': 'object',
    'USERS': 'object'
}

# The column spec is then used to apply the correct types after loading the initial dataframe
asset_file_column_spec = {
    'NAME': 'string',
    'IMPACT': 'int64',
    'LIKELIHOOD': 'int64',
    'RISK': 'int64',
    'MAC Addresses': 'string',
    'IP Addresses': 'string',
    'SERIAL NUMBER': 'string',
    'GEO LOCATION': 'category',
    'ASSET TYPE': 'category',
    'ASSET SUBTYPE': 'category',
    'OPERATING SYSTEM': 'category',
    'OS PATCH STATUS': 'category',
    'LAST PATCH DATE': 'datetime64[ns, UTC]',
    'MANUFACTURER': 'category',
    'SITE': 'category',
    'LAST OBSERVED': 'datetime64[ns, UTC]',
    'FIRST OBSERVED': 'datetime64[ns, UTC]',
    'LAST PROCESSED': 'datetime64[ns, UTC]',
    'Roles': 'object',
    'Ports': 'object',
    'TAGS': 'object',
    'Interface Info (IP,MAC,SUBNET,VLAN)': 'object',
    'ACTIVE ISSUES': 'int64',
    'CVEs': 'int64',
    'REBOOT PENDING STATUS': 'category',
    'UPTIME IN DAYS': 'int64',
    'OBSERVERS': 'object',
    'USERS': 'object'
}

def read_asset_csv(source):
    df = pd.read_csv(source, dtype=asset_file_import_spec)
    return df

def read_asset_file(source):
    # Initialize an empty list to store dataframes
    dataframes = []
    use_cols = list(asset_file_import_spec.keys())
    
    # Open the ZIP file
    with zipfile.ZipFile(source, 'r') as z:
        # List all contained files
        for file_info in z.infolist():
            # Check if 'cve_export' is in the file path and it's a CSV
            if file_info.filename.endswith('.csv'):
                # Read the file from the archive directly
                with z.open(file_info) as file:
                    # BytesIO allows pandas to read from bytes like it's reading from a file
                    df_from_zip = pd.read_csv(BytesIO(file.read()), dtype=asset_file_import_spec, usecols=use_cols)
                    dataframes.append(df_from_zip)
    
    # Concatenate all dataframes into a single dataframe
    df = pd.concat(dataframes, ignore_index=True)
    
    return df

def convert_asset_df(df):

    string_columns = {'NAME', 'MAC Addresses', 'IP Addresses', 'SERIAL NUMBER'}
    for column in string_columns:
        df[column] = df[column].astype('string')
        
    # Replace 'Unknown' with 0 in specified columns
    integer_columns = {'ACTIVE ISSUES', 'CVEs', 'UPTIME IN DAYS'}
    for column in integer_columns:
        df[column] = df[column].replace('Unknown', 0).astype(int)

    # Replace Unknown Risk, Likelihood, and Imapct with -1 since we don't want 0s
    rli_columns = {'RISK', 'LIKELIHOOD', 'IMPACT'}
    for column in rli_columns:
        df[column] = df[column].replace('Unknown', -1).astype(int)

    # Convert to datetime, coercing errors and handling None, NaN, and empty strings
    datetime_columns = {'FIRST OBSERVED', 'LAST OBSERVED', 'LAST PATCH DATE', 'LAST PROCESSED'}
    for column in datetime_columns:
        df[column] = pd.to_datetime(df[column], errors='coerce', utc=True)

        # Fill NaT values with a specific default timestamp, considering time zone
        default_timestamp = pd.Timestamp('1970-01-01 00:00:00+00:00')
        df[column] = df[column].fillna(default_timestamp)
    
    # list conversion
    list_columns = {'TAGS', 'Roles', 'Ports', 'USERS', 'OBSERVERS'}
    for column in list_columns:
        df[column] = df[column].apply(convert_string_to_list)

    # Fill NaN Tags
    df['TAGS'] = df['TAGS'].apply(lambda x: ['Untagged:Untagged'] if x is None or (isinstance(x, list) and len(x) == 0) else x)

    # list of dictionary conversion
    df['Interface Info (IP,MAC,SUBNET,VLAN)'] = df['Interface Info (IP,MAC,SUBNET,VLAN)'].apply(convert_str_to_objects)

    category_columns = {'GEO LOCATION', 'ASSET TYPE', 'ASSET SUBTYPE', 'OPERATING SYSTEM', 'OS PATCH STATUS', 'MANUFACTURER', 'SITE', 'REBOOT PENDING STATUS'}
    for column in category_columns:
        df[column] = df[column].astype('category')
    
    # Validate data types
    for column, expected_dtype in asset_file_column_spec.items():
        if df[column].dtype != expected_dtype:
            actual_dtype = df[column].dtype
            raise ValueError(f"Data type mismatch in column '{column}': expected {expected_dtype}, got {actual_dtype}")

    return df


# # # # # # # # # # # # # # #
# CVE Standard Export Loaders
# # # # # # # # # # # # # # #

# The import spec ensures proper handling of data types while the file is being read; important for large datasets
# Commented lines will not be imported
cve_file_import_spec = {
    'ASSET NAME': 'object',
    'SOFTWARE': 'object',
    'CVE-ID': 'object',
    'PUBLISHED DATE (UTC)': 'object',
    'CVSS 3.x': 'float64',
    'SEVERITY': 'object',
    'CVE DESCRIPTION': 'object'
}

def read_cve_file(source):
    """
    Reads CSV files from a ZIP archive and returns a concatenated DataFrame.
    """
    # List to store DataFrames
    dataframes = []
    use_cols = list(cve_file_import_spec.keys())

    # Open the ZIP file
    with zipfile.ZipFile(source, 'r') as z:
        # List all contained files
        for file_info in z.infolist():
            # Check if the file is a CSV
            if file_info.filename.endswith('.csv'):
                # Read the file from the archive directly
                with z.open(file_info) as file:
                    df_from_zip = pd.read_csv(
                        BytesIO(file.read()),
                        dtype=cve_file_import_spec,
                        usecols=use_cols
                    )
                    dataframes.append(df_from_zip)
    
    # Concatenate all dataframes into a single dataframe
    df = pd.concat(dataframes, ignore_index=True)
    
    return df

# The column spec is then used to apply the correct types after loading the initial dataframe
cve_file_column_spec = {
    'ASSET NAME': 'category',
    'SOFTWARE': 'category',
    'CVE-ID': 'category',
    'PUBLISHED DATE (UTC)': 'datetime64[ns, UTC]',
    'CVSS 3.x': 'float64',
    'SEVERITY': 'category',
    'CVE DESCRIPTION': 'category'
}

def convert_cve_df(df):
    string_columns = {}
    for column in string_columns:
        df[column] = df[column].astype('string')
    
    float_columns = {'CVSS 3.x'}
    for column in float_columns:
        df[column] = df[column].astype('float64')
        
    # Replace 'Unknown' with 0 in specified columns
    # integer_columns = {'Balbix Score', 'Balbix Rank'}
    # for column in integer_columns:
    #     df[column] = df[column].replace('Unknown', 0).astype(int)
    
    category_columns = {'ASSET NAME', 'SOFTWARE', 'CVE-ID', 'SEVERITY', 'CVE DESCRIPTION'}
    for column in category_columns:
        df[column] = df[column].astype('category')

    # Convert to datetime, coercing errors and handling None, NaN, and empty strings
    datetime_columns = {'PUBLISHED DATE (UTC)'}
    for column in datetime_columns:
        df[column] = pd.to_datetime(df[column], errors='coerce', utc=True)

        # Fill NaT values with a specific default timestamp, considering time zone
        default_timestamp = pd.Timestamp('1970-01-01 00:00:00+00:00')
        df[column] = df[column].fillna(default_timestamp)

    # Validate data types
    for column, expected_dtype in cve_file_column_spec.items():
        if df[column].dtype != expected_dtype:
            actual_dtype = df[column].dtype
            raise ValueError(f"Data type mismatch in column '{column}': expected {expected_dtype}, got {actual_dtype}")
    
    return df


# # # # # # # # # # # # # # #
# CVE Tactical Export Loaders
# # # # # # # # # # # # # # #

# The import spec ensures proper handling of data types while the file is being read; important for large datasets
# Commented lines will not be imported
tactical_cve_file_import_spec = {
    # 'ID': 'int64',
    'Name': 'string',
    # 'Roles': 'object',
    # 'Tags': 'object',
    # 'IP Address': 'string',
    # 'MAC Address': 'string',
    # 'Operating System': 'object',
    'Product': 'object',
    'Vendor': 'object',
    'Version': 'object',
    'Product Type': 'object',
    'Strategic Fix': 'object',
    'Tactical Fixes': 'object',
    'CVE': 'object',
    'CVSS Version 2.0 Score': 'object',
    'CVSS Version 2.0 Severity': 'object',
    'CVSS Version 3.x Score': 'object',
    'CVSS Version 3.x Severity': 'object',
    'CVE Tag': 'object',
    # 'Interface info (IP, MAC)': 'object',
    'First Detected Time': 'object',
    'Balbix Score': 'int64',
    'Balbix Rank': 'int64',
    'Risk Accepted': 'object'
}

# The column spec is then used to apply the correct types after loading the initial dataframe
tactical_cve_file_column_spec = {
    # 'ID': 'int64',
    'Name': 'category',
    # 'Roles': 'object',
    # 'Tags': 'object',
    # 'IP Address': 'string',
    # 'MAC Address': 'string',
    # 'Operating System': 'category',
    'Product': 'category',
    'Vendor': 'category',
    'Version': 'category',
    'Product Type': 'category',
    'Strategic Fix': 'category',
    'Tactical Fixes': 'category',
    'CVE': 'category',
    'CVSS Version 2.0 Score': 'float64',
    'CVSS Version 2.0 Severity': 'category',
    'CVSS Version 3.x Score': 'float64',
    'CVSS Version 3.x Severity': 'category',
    'CVE Tag': 'object',
    # 'Interface info (IP, MAC)': 'object',
    'First Detected Time': 'object',
    'Balbix Score': 'int64',
    'Balbix Rank': 'int64',
    'Risk Accepted': 'category'
}

def read_tactical_cve_file(source):
    # Initialize an empty list to store dataframes
    dataframes = []
    use_cols = list(tactical_cve_file_import_spec.keys())
    
    # Open the ZIP file
    with zipfile.ZipFile(source, 'r') as z:
        # List all contained files
        for file_info in z.infolist():
            # Check if 'cve_export' is in the file path and it's a CSV
            if 'report' in file_info.filename and file_info.filename.endswith('.csv'):
                # Read the file from the archive directly
                with z.open(file_info) as file:
                    # BytesIO allows pandas to read from bytes like it's reading from a file
                    df_from_zip = pd.read_csv(BytesIO(file.read()), dtype=tactical_cve_file_import_spec, usecols=use_cols)
                    dataframes.append(df_from_zip)
    
    # Concatenate all dataframes into a single dataframe
    df = pd.concat(dataframes, ignore_index=True)
    
    return df

def convert_tactical_cve_df(df):
    # string_columns = {'Name'}
    # for column in string_columns:
    #     df[column] = df[column].astype('string')
    
    float_columns = {'CVSS Version 2.0 Score', 'CVSS Version 3.x Score'}
    for column in float_columns:
        df[column] = df[column].astype('float64')
        
    # Replace 'Unknown' with 0 in specified columns
    integer_columns = {'Balbix Score', 'Balbix Rank'}
    for column in integer_columns:
        df[column] = df[column].replace('Unknown', 0).astype(int)
    
    category_columns = {'Name', 'Product', 'Vendor', 'Version', 'Product Type', 'Strategic Fix', 'Tactical Fixes', 'CVE', 'CVSS Version 2.0 Severity', 'CVSS Version 3.x Severity', 'Risk Accepted'}
    for column in category_columns:
        df[column] = df[column].astype('category')

    # Validate data types
    for column, expected_dtype in tactical_cve_file_column_spec.items():
        if df[column].dtype != expected_dtype:
            actual_dtype = df[column].dtype
            raise ValueError(f"Data type mismatch in column '{column}': expected {expected_dtype}, got {actual_dtype}")
    
    return df
