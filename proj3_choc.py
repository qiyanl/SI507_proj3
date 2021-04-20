import sqlite3
import pandas as pd
from prettytable import PrettyTable
import re
import plotly
import plotly.graph_objs as go


# proj3_choc.py
# You can change anything in this file you want as long as you pass the tests
# and meet the project requirements! You will need to implement several new
# functions.

# Part 0: Read data from a database called choc.db
DBNAME = 'choc.sqlite'
conn = sqlite3.connect(DBNAME)
cur = conn.cursor()

# Part 1: Implement logic to process user commands


def process_bars(command):
    ''' If the first element in the command is 'bars',this function will be
    used and return a set of records, each represents a particular
    chocolate bar.
    
    Parameters
    ----------
    command: str
        The command to process
    
    Returns
    -------
    list:
        Return a list of tuples, each tuple represents a particular chocolate bar.
    '''
    command_0 = command.split(' ')
    if '=' in command:
        command_1 = command.split('=')
        command_2 = command_1[0].split(' ')
        command_3 = command_1[1].split(' ')
    else:
        command_2 = command_0
    
    if 'source' in command:
        source = 'source'
    else:
        source = 'sell'
    
    if 'region' in command:
        spec_loc = 'region'
    elif 'country' in command:
        spec_loc = 'country'
    else:
        spec_loc = None
    
    if 'bottom' in command:
        sort_order = 'ASC'
    else:
        sort_order = 'DESC'
    
    if 'cocoa' in command:
        order_type = 'CocoaPercent'       
    else:
        order_type = 'Rating'

    if (command.split(' ')[-1]).isnumeric():
        len_num = int(command.split(' ')[-1])
    else:
        len_num = 10

    if spec_loc == 'country':
        query = "SELECT Id FROM Countries WHERE Alpha2='%s'" % command_3[0]
        cur.execute(query)
        coun_id = cur.fetchall()[0][0]
        # print(coun_id)
        if source == 'source':
            query = "SELECT SpecificBeanBarName, Company, CompanyLocationId, Rating,CocoaPercent,BroadBeanOriginId FROM Bars WHERE BroadBeanOriginId='%s' order by %s %s" % (coun_id,order_type,sort_order)
            cur.execute(query)
        if source == 'sell':
            query = "SELECT SpecificBeanBarName, Company, CompanyLocationId, Rating,CocoaPercent,BroadBeanOriginId FROM Bars WHERE CompanyLocationId='%s' order by %s %s" % (coun_id,order_type,sort_order)     
            cur.execute(query)
        bean_name =[]
        com_name = []
        com_id = []
        rating = []
        coco_per = []
        ori_id = []
        alldata = cur.fetchall()
        for item in alldata:
            bean_name.append(item[0])
            com_name.append(item[1])
            com_id.append(item[2])
            rating.append(item[3])
            coco_per.append(item[4])
            ori_id.append(item[5])

        comp_loc = []
        for id in com_id:
            query = "select EnglishName FROM Countries where Id ='%s'" % id
            cur.execute(query)
            comp_loc.append(cur.fetchall()[0][0])
        ori_name = []
        for id in ori_id:
            query = "select EnglishName FROM Countries where Id ='%s'" % id
            cur.execute(query)
            ori_name.append(cur.fetchall()[0][0])
        
        coun_result = []
        for i in range(len(alldata)):
            temp = ((bean_name[i]),(com_name[i]),(comp_loc[i]),(rating[i]),(coco_per[i]),(str(ori_name[i])))
            coun_result.append(temp)
        if order_type == 'Rating':
            if sort_order == 'DESC':
                bars_final_output = sorted(coun_result,key=lambda x:(x[3]),reverse=True)
            if sort_order == 'ASC':
                bars_final_output = sorted(coun_result,key=lambda x:(x[3]))
        if order_type =='CocoaPercent':
            if sort_order == 'DESC':
                bars_final_output = sorted(coun_result,key=lambda x:(x[4]),reverse=True)
            if sort_order == 'ASC':
                bars_final_output = sorted(coun_result,key=lambda x:(x[4]))
        
        return bars_final_output[0:len_num]

    elif spec_loc == 'region':
        query = "SELECT Id FROM Countries WHERE Region='%s'" % command_3[0]
        cur.execute(query)
        reg_id = cur.fetchall()
        region_id_list = []
        for id in reg_id:
            region_id_list.append(id[0])
        # print(region_id_list)
        bean_name =[]
        com_name = []
        com_id = []
        rating = []
        coco_per = []
        ori_id = []
        raw_reg_res = []

        for id in region_id_list:
            if source == 'source':
                query = "SELECT SpecificBeanBarName, Company, CompanyLocationId, Rating,CocoaPercent,BroadBeanOriginId FROM Bars WHERE BroadBeanOriginId='%s' order by %s %s" % (id,order_type,sort_order)
                cur.execute(query)
            if source == 'sell':
                query = "SELECT SpecificBeanBarName, Company, CompanyLocationId, Rating,CocoaPercent,BroadBeanOriginId FROM Bars WHERE CompanyLocationId='%s' order by %s %s" % (id,order_type,sort_order)
                cur.execute(query)
            
            alldata = cur.fetchall()
            if alldata !=[]:
                raw_reg_res.append(alldata)
        # print(raw_reg_res)
        for item in raw_reg_res:
            # print(item)
            for i in range(len(item)):
                bean_name.append(item[i][0])
                com_name.append(item[i][1])
                com_id.append(item[i][2])
                rating.append(item[i][3])
                coco_per.append(item[i][4])
                ori_id.append(item[i][5])
        # print(com_id)
        comp_loc = []
        for id in com_id:
            query = "select EnglishName FROM Countries where Id ='%s'" % id
            cur.execute(query)
            comp_loc.append(cur.fetchall()[0][0])
        ori_name = []
        for id in ori_id:
            query = "select EnglishName FROM Countries where Id ='%s'" % id
            cur.execute(query)
            ori_name.append(cur.fetchall()[0][0])
        # print(ori_name)
        region_result = []
        for i in range(len(com_id)):
            temp = ((bean_name[i]),(com_name[i]),(comp_loc[i]),(rating[i]),(coco_per[i]),(str(ori_name[i])))
            region_result.append(temp)
        
        if order_type =='CocoaPercent':
            if sort_order == 'DESC':
                bars_final_output = sorted(region_result,key=lambda x:(x[4]),reverse=True)
            if sort_order == 'ASC':
                bars_final_output = sorted(region_result,key=lambda x:(x[4]))
        else:
            if sort_order == 'DESC':
                bars_final_output = sorted(region_result,key=lambda x:(x[3]),reverse=True)
            if sort_order == 'ASC':
                bars_final_output = sorted(region_result,key=lambda x:(x[3]))
    else:
        query ="select SpecificBeanBarName,Company,CompanyLocationId,Rating,CocoaPercent,BroadBeanOriginId from Bars order by %s %s" % (order_type,sort_order)
        cur.execute(query)
        alldata = cur.fetchall()

        bean_name =[]
        com_name = []
        com_id = []
        rating = []
        coco_per = []
        ori_id = []
        for item in alldata:
            bean_name.append(item[0])
            com_name.append(item[1])
            com_id.append(item[2])
            rating.append(item[3])
            coco_per.append(item[4])
            ori_id.append(item[5])
        # print(com_id)
        comp_loc = []
        for id in com_id:
            query = "select EnglishName FROM Countries where Id ='%s'" % id
            cur.execute(query)
            comp_loc.append(cur.fetchall()[0][0])
        ori_name = []
        for id in ori_id:
            query = "select EnglishName FROM Countries where Id ='%s'" % id
            cur.execute(query)
            ori_name.append(cur.fetchall()[0][0])
        # print(ori_name)
        region_result = []
        for i in range(len(com_id)):
            temp = ((bean_name[i]),(com_name[i]),(comp_loc[i]),(rating[i]),(coco_per[i]),(str(ori_name[i])))
            region_result.append(temp)
        
        if order_type =='CocoaPercent':
            if sort_order == 'DESC':
                bars_final_output = sorted(region_result,key=lambda x:(x[4]),reverse=True)
            if sort_order == 'ASC':
                bars_final_output = sorted(region_result,key=lambda x:(x[4]))
        else:
            if sort_order == 'DESC':
                bars_final_output = sorted(region_result,key=lambda x:(x[3]),reverse=True)
            if sort_order == 'ASC':
                bars_final_output = sorted(region_result,key=lambda x:(x[3]))

    return bars_final_output[0:len_num]
    

def process_companies(command):
    ''' If the first element in the command is 'companies',this function will be
    used and return a set of records representing different companies.
    
    Parameters
    ----------
    command: str
        The command to process
    
    Returns
    -------
    list:
        Return a list of tuples, each tuple represents a particular company.
    '''

    command_0 = command.split(' ')
    if '=' in command:
        command_1 = command.split('=')
        command_2 = command_1[0].split(' ')
        command_3 = command_1[1].split(' ')
    else:
        command_2 = command_0
    
    if 'region' in command:
        spec_loc = 'region'
    elif 'country' in command:
        spec_loc = 'country'
    else:
        spec_loc = None
    
    if 'bottom' in command:
        sort_order = 'ASC'
    else:
        sort_order = 'DESC'
    
    if 'cocoa' in command:
        order_type = 'AVG(CocoaPercent)'       
    elif 'number_of_bars' in command:
        order_type = 'COUNT(Id)'
    else:
        order_type = 'AVG(Rating)'

    if (command.split(' ')[-1]).isnumeric():
        len_num = int(command.split(' ')[-1])
    else:
        len_num = 10

    all_data = []
    if spec_loc == 'region':
        query = "SELECT Id, EnglishName FROM Countries WHERE Region='%s'" % command_3[0]
        cur.execute(query)
        reg_id = cur.fetchall()
        region_id_list = []
        for id in reg_id:
            region_id_list.append(id[0])
        # print(region_id_list)
        for region_id in region_id_list:
            query = "SELECT Company,CompanyLocationId,COUNT(Id),AVG(Rating),AVG(CocoaPercent) from bars where CompanyLocationId ='%s' group by Company order by %s %s" % (region_id,order_type,sort_order)
            cur.execute(query)
            temp_data = cur.fetchall()
            if temp_data !=[]:
                all_data.append(temp_data)
        # print(all_data)
    
    elif spec_loc == 'country':
        query = "SELECT Id, EnglishName FROM Countries WHERE Alpha2='%s'" % command_3[0]
        cur.execute(query)
        country_id = cur.fetchall()[0][0]
        # print(country_id)
        query = "SELECT Company,CompanyLocationId,COUNT(Id),AVG(Rating),AVG(CocoaPercent) from bars where CompanyLocationId ='%s' group by Company order by %s %s" % (country_id,order_type,sort_order)
        cur.execute(query)
        temp_data = cur.fetchall()
        if temp_data !=[]:
                all_data.append(temp_data)

    elif spec_loc == None:
        query ="SELECT Company,CompanyLocationId,COUNT(Id),AVG(Rating),AVG(CocoaPercent) from bars group by Company order by %s %s" % (order_type,sort_order)
        cur.execute(query)
        temp_data = cur.fetchall()
        if temp_data !=[]:
                all_data.append(temp_data)
    # print(all_data)
        
    com_name = []
    com_id = []
    rating = []
    num_bars = []
    coco_per = []
    # print(all_data)
    # print(all_data[0][0])
    for item in all_data:
        for i in range(len(item)):
            if int(item[i][2]) > 4:
                com_name.append(item[i][0])
                com_id.append(item[i][1])
                num_bars.append(item[i][2])
                rating.append(round(item[i][3],2))
                coco_per.append(round(item[i][4],2))
    # print(coco_per)
    # print(com_name)
    comp_loc = []
    for id in com_id:
        query = "select EnglishName FROM Countries where Id ='%s'" % id
        cur.execute(query)
        comp_loc.append(cur.fetchall()[0][0])
    raw_result = []
        
    if order_type == 'AVG(Rating)':
        for i in range(len(comp_loc)):
            temp = (com_name[i],comp_loc[i],rating[i])
            raw_result.append(temp)
        if order_type == 'DESC':
            final_result = sorted(raw_result,key=lambda x:(x[2]))
        else:
            final_result = sorted(raw_result,key=lambda x:(x[2]),reverse=True)
        
    
    elif order_type == 'AVG(CocoaPercent)':
        for i in range(len(comp_loc)):
            temp = ((com_name[i]),(comp_loc[i]),(coco_per[i]))
            # print(temp)
            raw_result.append(temp)
        if sort_order == 'DESC':
            final_result = sorted(raw_result,key=lambda x:(x[2]),reverse=True)
        else:
            final_result = sorted(raw_result,key=lambda x:(x[2]))

    
    elif order_type == 'COUNT(Id)':
        for i in range(len(comp_loc)):
            temp = ((com_name[i]),(comp_loc[i]),(num_bars[i]))
            # print(temp)
            raw_result.append(temp)
        if sort_order == 'DESC':
            final_result = sorted(raw_result,key=lambda x:(x[2]),reverse=True)
        else:
            final_result = sorted(raw_result,key=lambda x:(x[2]))
    # print(final_result[0:len_num])
    return final_result[0:len_num]
    
def process_countries(command):
    ''' If the first element in the command is 'countries',this function will be
    used and return a set of records representing different countries.
    
    Parameters
    ----------
    command: str
        The command to process
    
    Returns
    -------
    list:
        Return a list of tuples, each tuple represents a particular country.
    '''

    command_0 = command.split(' ')
    if '=' in command:
        command_1 = command.split('=')
        command_2 = command_1[0].split(' ')
        command_3 = command_1[1].split(' ')
    else:
        command_2 = command_0
    
    if 'source' in command:
        source = 'source'
    else:
        source = 'sell'
    # print(source)
    if 'region' in command:
        spec_loc = 'region'
    else:
        spec_loc = None
    
    if 'bottom' in command:
        sort_order = 'ASC'
    else:
        sort_order = 'DESC'
    
    if (command.split(' ')[-1]).isnumeric():
        len_num = int(command.split(' ')[-1])
    else:
        len_num = 10
    
    if 'cocoa' in command:
        order_type = 'AVG(CocoaPercent)'       
    elif 'number_of_bars' in command:
        order_type = 'COUNT(Id)'
    else:
        order_type = 'AVG(Rating)'
    # print(order_type)

    if spec_loc == 'region':
        query = "SELECT Id,Alpha2,EnglishName,Region from countries where Region='%s'" % command_3[0]
        cur.execute(query)
        countries_data = cur.fetchall()
        country_id_list = []
        for item in countries_data:
            country_id_list.append(item[0]) 
    elif spec_loc == None:
        query = "SELECT Id,Alpha2,EnglishName,Region from countries"
        cur.execute(query)
        countries_data = cur.fetchall()
        country_id_list = []
        for item in countries_data:
            country_id_list.append(item[0]) 
    # print(country_id_list)
    
    region_all_data =[]
    if source == 'sell':
        for id in country_id_list:
            query = "SELECT Company,CompanyLocationId,COUNT(Id),AVG(Rating),AVG(CocoaPercent) from bars where CompanyLocationId ='%s' group by CompanyLocationId order by %s %s" % (id,order_type,sort_order)
            cur.execute(query)
            region_data = cur.fetchall()
            if region_data != []:
                # print(region_data[0][2])
                if region_data[0][2] > 4:
                    region_all_data.append(region_data)
    # print(region_all_data)
    
    if source == 'source':
        for id in country_id_list:
            query = "SELECT Company,BroadBeanOriginId,COUNT(Id),AVG(Rating),AVG(CocoaPercent) from bars where BroadBeanOriginId ='%s' group by BroadBeanOriginId order by %s %s" % (id,order_type,sort_order)
            cur.execute(query)
            region_data = cur.fetchall()
            # print(region_data)
            if region_data !=[]:
                if region_data[0][2] > 4:
                    region_all_data.append(region_data)
    # print(region_all_data)
    
    comp_loc_id = []
    count_id = []
    avg_rate = []
    avg_coco = []
    for item in region_all_data:
        comp_loc_id.append(item[0][1])
        count_id.append(item[0][2])
        avg_rate.append(item[0][3])
        avg_coco.append(item[0][4])
    # print(comp_loc_id)
    country_name =[]
    region_name = []
    for id in comp_loc_id:
        query="select EnglishName, Region from Countries where Id = %s"%id
        cur.execute(query)
        temp = cur.fetchall()
        # print(temp)
        country_name.append(temp[0][0])
        region_name.append(temp[0][1])

    raw_result = []    
    if order_type == 'AVG(Rating)':
        for i in range(len(comp_loc_id)):
            temp = ((country_name[i]),(region_name[i]),(avg_rate[i]))
            raw_result.append(temp)
        # print(raw_result)
        if sort_order == 'DESC':
            final_result = sorted(raw_result,key=lambda x:(x[2]),reverse=True)
        else:
            final_result = sorted(raw_result,key=lambda x:(x[2]))
        
    
    elif order_type == 'AVG(CocoaPercent)':
        for i in range(len(comp_loc_id)):
            temp = ((country_name[i]),(region_name[i]),(avg_coco[i]))
            # print(temp)
            raw_result.append(temp)
        if sort_order == 'DESC':
            final_result = sorted(raw_result,key=lambda x:(x[2]),reverse=True)
        else:
            final_result = sorted(raw_result,key=lambda x:(x[2]))

    
    elif order_type == 'COUNT(Id)':
        for i in range(len(comp_loc_id)):
            temp = ((country_name[i]),(region_name[i]),(count_id[i]))
            # print(temp)
            raw_result.append(temp)
        if sort_order == 'DESC':
            final_result = sorted(raw_result,key=lambda x:(x[2]),reverse=True)
        else:
            final_result = sorted(raw_result,key=lambda x:(x[2]))
    
    
    return final_result[0:len_num]

def process_regions(command):
    ''' If the first element in the command is 'regions',this function will be
    used and return a set of records representing different regions.
    
    Parameters
    ----------
    command: str
        The command to process
    
    Returns
    -------
    list:
        Return a list of tuples, each tuple represents a particular region.
    '''

    command_0 = command.split(' ')
    if '=' in command:
        command_1 = command.split('=')
        command_2 = command_1[0].split(' ')
        command_3 = command_1[1].split(' ')
    else:
        command_2 = command_0
    
    if 'source' in command:
        source = 'source'
    else:
        source = 'sell'

    if 'cocoa' in command:
        order_type = 'AVG(CocoaPercent)'       
    elif 'number_of_bars' in command:
        order_type = 'count(Countries.Id)'
    else:
        order_type = 'AVG(Rating)'
    
    if (command.split(' ')[-1]).isnumeric():
        len_num = int(command.split(' ')[-1])
    else:
        len_num = 10

    region_list = ['Europe','Africa','Oceania','Polar','Asia','Americas','No Region',' ']
    primary_coco = []
    primary_rate = []
    count_id = []
    region_name_list = []
    region_all_list = []
    if source == 'source':
        for name in region_list:
            query = "select Countries.Region,Countries.Id,bars.BroadBeanOriginId,avg(bars.CocoaPercent),avg(bars.Rating),count(Countries.Id) from Bars,Countries where bars.BroadBeanOriginId=Countries.Id and Countries.Region='%s' group by Region "%(name)
            cur.execute(query)
            temp_data = cur.fetchall()
            if temp_data != []:
                for item in temp_data:
                    if item[-1] >4:
                        primary_coco.append(item[3])
                        primary_rate.append(item[-2])
                        count_id.append(item[-1])
                        region_name_list.append(item[0])

    if source == 'sell':
        for name in region_list:
            query = "select Countries.Region,Countries.Id,bars.CompanyLocationId,avg(bars.CocoaPercent),avg(bars.Rating),count(Countries.Id) from Bars,Countries where bars.CompanyLocationId=Countries.Id and Countries.Region='%s' group by Region "%(name)
            cur.execute(query)
            temp_data = cur.fetchall()
            if temp_data != []:
                for item in temp_data:
                    if item[-1] >4:
                        primary_coco.append(item[3])
                        primary_rate.append(item[-2])
                        count_id.append(item[-1])
                        region_name_list.append(item[0])
    
    if order_type =='AVG(Rating)':
        for i in range(len(region_name_list)):
            temp =((region_name_list[i]),(primary_rate[i]))
            # print(temp)
            region_all_list.append(temp)
        if order_type == 'DESC':
            final_result = sorted(region_all_list,key=lambda x:(x[1]))
        else:
            final_result = sorted(region_all_list,key=lambda x:(x[1]),reverse=True)
    if order_type =='AVG(CocoaPercent)':
        for i in range(len(region_name_list)):
            temp =((region_name_list[i]),(primary_coco[i]))
            region_all_list.append(temp)
        if order_type == 'DESC':
            final_result = sorted(region_all_list,key=lambda x:(x[1]))
        else:
            final_result = sorted(region_all_list,key=lambda x:(x[1]),reverse=True)
    if order_type =='count(Countries.Id)':
        for i in range(len(region_name_list)):
            temp =((region_name_list[i]),(count_id[i]))
            region_all_list.append(temp)
        if order_type == 'DESC':
            final_result = sorted(region_all_list,key=lambda x:(x[1]))
        else:
            final_result = sorted(region_all_list,key=lambda x:(x[1]),reverse=True)
    
    return final_result[0:len_num]

def process_command(command):
    '''This function takes a string and returns a list of tuples
    according to the options provided in the command string.
    
    Parameters
    ----------
    command: str
        The command to process
    
    Returns
    -------
    list:
        Return a list of tuples, 
        each tuple represents a particular bar or company or country or region
        according to the high level command in the command string.
    '''
    command_0 = command.split(' ')
    if '=' in command:
        command_1 = command.split('=')
        command_2 = command_1[0].split(' ')
        command_3 = command_1[1].split(' ')
    else:
        command_2 = command_0
    
    if command_2[0]=='bars':
        final_out = process_bars(command)
    elif command_2[0]=='companies':
        final_out = process_companies(command)
    elif command_2[0]=='countries':
        final_out = process_countries(command)
    elif command_2[0]=='regions':
        final_out = process_regions(command)
    
    return final_out
    

def load_help_text():
    '''Read and load the 'Proj3Help.txt' file.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    Load the 'Proj3Help.txt' file.
    '''
    with open('Proj3Help.txt') as f:
        return f.read()

def command_to_table(command):
    '''This function takes a list of tuples returned by
    process_command() function and returns a pretty table.
    
    Parameters
    ----------
    command: str
        The command to process
    
    Returns
    -------
    table:
        Return a pretty table, each row reprents a tuple.
    '''
    raw_result = process_command(command)
    x = PrettyTable()
    temp_row = []
    for item in raw_result:
        temp_row = []
        for i in range(len(item)):
            if isinstance(item[i],str):
                if len(item[i])>12:
                    temp = item[i][0:12]+'...'
                else:
                    temp = item[i]
            elif isinstance(item[i],float) and item[i]<1:
                temp = format(item[i],'.0%')
            else:
                temp = item[i]
            temp_row.append(temp)
        x.add_row(temp_row)
    print(x)


# Part 2 & 3: Implement interactive prompt and plotting. We've started for you!
def interactive_prompt():
    '''This function allows a user to interactively input commands,
    and to nicely format the result for presentation and visualization.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    a nicely format table or a barplot:
        If 'barplot' is not in the command, it will return a nicely format table.
        If 'barplot' is in the command, it will return a barplot according the parameter
        provided in the command string.
    '''
    help_text = load_help_text()
    response = ''
    while response != 'exit':
        response = input('Enter a command: ')
        if response == 'exit':
            exit()
        elif response == 'help':
            print(help_text)
            continue
        
        elif 'barplot' in response:
            command_to_list = re.findall(r"(.+?) barplot",response)
            result_list = process_command(command_to_list[0])
            # print(result_list)
            command_split = response.split(' ')
            if command_split[0] == 'bars':
                temp_df = pd.DataFrame(result_list)
                # print(temp_df)
                if 'cocoa' in response:
                    barplot_bars = go.Bar(x=temp_df[0],y=temp_df[4])
                    fig = go.Figure(barplot_bars)
                    fig.show()
                else:
                    barplot_bars = go.Bar(x=temp_df[0],y=temp_df[3])
                    fig = go.Figure(barplot_bars)
                    fig.show()
            
            elif command_split[0] == 'companies':
                temp_df = pd.DataFrame(result_list)
                # print(temp_df)
                if 'cocoa' in response:
                    barplot_bars = go.Bar(x=temp_df[0],y=temp_df[2])
                    fig = go.Figure(barplot_bars)
                    fig.show()
                elif 'number_of_bars' in response:
                    barplot_bars = go.Bar(x=temp_df[0],y=temp_df[2])
                    fig = go.Figure(barplot_bars)
                    fig.show() 
                else:
                    barplot_bars = go.Bar(x=temp_df[0],y=temp_df[2])
                    fig = go.Figure(barplot_bars)
                    fig.show()
            
            elif command_split[0] == 'countries':
                temp_df = pd.DataFrame(result_list)
                # print(temp_df)
                if 'cocoa' in response:
                    barplot_bars = go.Bar(x=temp_df[0],y=temp_df[2])
                    fig = go.Figure(barplot_bars)
                    fig.show()
                elif 'number_of_bars' in response:
                    barplot_bars = go.Bar(x=temp_df[0],y=temp_df[2])
                    fig = go.Figure(barplot_bars)
                    fig.show() 
                else:
                    barplot_bars = go.Bar(x=temp_df[0],y=temp_df[2])
                    fig = go.Figure(barplot_bars)
                    fig.show() 
                
            
            elif command_split[0] == 'regions':
                temp_df = pd.DataFrame(result_list)
                # print(temp_df)
                if 'cocoa' in response:
                    barplot_bars = go.Bar(x=temp_df[0],y=temp_df[1])
                    fig = go.Figure(barplot_bars)
                    fig.show()
                elif 'number_of_bars' in response:
                    barplot_bars = go.Bar(x=temp_df[0],y=temp_df[1])
                    fig = go.Figure(barplot_bars)
                    fig.show() 
                else:
                    barplot_bars = go.Bar(x=temp_df[0],y=temp_df[1])
                    fig = go.Figure(barplot_bars)
                    fig.show()   
        else:
            try:
                command_to_table(response)
            except:
                print('Command not recognized: {}'.format(response))

        

# Make sure nothing runs or prints out when this file is run as a module/library
if __name__=="__main__":
    interactive_prompt()
    


