# Imports
import re
import copy
import math
import json
import joblib
import pickle
import random
import functools
import numpy                    as np
import pandas                   as pd
import seaborn                  as sn
import matplotlib.pyplot        as plt
import matplotlib.font_manager  as fm

from os                         import scandir, getcwd
from pandas                     import DataFrame
from sklearn                    import preprocessing
from matplotlib.collections     import QuadMesh


# Lambda functions

flatten_list        = lambda t: [item for sublist in t for item in sublist]
formatter_sentences = lambda x, y: "{}\n{}".format(x,y)
gen_dict_from_int   = lambda x: {item:0 for item in range(x)}

sum_funct               = lambda x, y: x+y
variance_funct          = lambda x, m: (x - m) ** 2

coordinates_oper        = lambda x1, x2: math.pow((x2 - x1), 2)
distance_between_points = lambda p1, p2: math.sqrt(functools.reduce(sum_funct, map(coordinates_oper, p1, p2)))
# Regular expressions

_re_words           = re.compile(r"[a-zA-ZáéíóúÁÉÍÓÚ]*")
_re_digits          = re.compile(r"[\d|\d\.]*")

# Data analysis tools

## Dataset related tools
def print_columns_names(df):
    for col_index, col_name in enumerate(df.columns):
        print("{} -> {}".format(col_index, col_name))

def show_columns_value(dataset:pd.DataFrame, cols_to_omit:list=[]):
    for column in list(dataset.columns):
    
        if (column not in cols_to_omit):
            print('Values in column {}:'.format(column))

            for value in dataset[column].unique():
                print('\t+ {}'.format(value))

def read_dataset(path, separator=","):
    """ Reads the dataset in csv format by defect (separator = ,)
    
    Parameters:
    path (str):         String path to the file in order to read it.

    separator (str):    String character that separates the data's columns.

    Returns:
    pandas DataFrame object with all the registers from the file pass.

    """

    return pd.read_csv(path, sep=separator)

def clean_and_normalize_data(data, exclude=[]):
    """ Cleans and normalize the data from a pandas DataFrame object

    Parameters:
    data (DataFrame):   pandas DataFrame object with the data to normalize

    exclude (list):     List with integer data that represents the columns
                        of the dataset to be excluded from normalized.

    Returns:
    A panda DataFrame object with the data normalized and cleaned of the
    columns that are indicated in exclude list.

    """

    df_ex           = data.loc[:, data.columns.difference(exclude)]
    df_labels       = data[exclude]

    columns         = df_ex.columns
    old_indexes     = df_ex.index.values

    
    min_max_scaler  = preprocessing.MinMaxScaler()
    df_norm         = min_max_scaler.fit_transform(df_ex)
    
    df_norm = pd.DataFrame(df_norm, columns = columns, index = old_indexes)

    df_norm = pd.concat([df_norm, df_labels], axis=1)

    return df_norm

def normalize_data(dataframe):
    """ Just normalize all the data in a pandas DataFrame object

    Parameters:
    dataframe (DataFrame): pandas DataFrame object with the data to normalize

    Returns:
    A pandas object with the data normalized

    """

    min_max_scaler      = preprocessing.MinMaxScaler()
    norm_values         = min_max_scaler.fit_transform(dataframe)
    
    dataframe_norm  = pd.DataFrame(data=norm_values, columns=dataframe.columns) 
     
    return dataframe_norm

def normalize_data_standardScaler(dataframe):
    min_max_scaler      = preprocessing.StandardScaler()
    norm_values         = min_max_scaler.fit_transform(dataframe)
    
    dataframe_norm  = pd.DataFrame(data=norm_values, columns=dataframe.columns) 
     
    return dataframe_norm

def divide_datasets(df_merged, percentage=0.67):
    
    df_divide = df_merged.sample(frac=1)
    df_train = df_divide[:int((len(df_divide))*percentage)]
    df_test = df_divide[int((len(df_divide))*percentage):]    
    
    return df_train, df_test

def divide_files(list_of_files, percentage=0.67):

    list_train  = []
    list_test   = []
    
    for i in range(len(list_of_files)):
        i_list = random.randint(1, 100)

        if i_list <= percentage * 100:
            list_train.append(list_of_files[i])
        else:
            list_test.append(list_of_files[i])

    return list_train, list_test

def to_csv(path,dataframe):
    dataframe.to_csv(path)

def insert_row_in_pos(pos, row_value, df):
	# Funciona con objetos de tipo Series de pandas.

    data_half_low, data_half_big = df[:pos], df[pos:]
    data_half_low = data_half_low.append(row_value, ignore_index = True)
    data_half_low = data_half_low.append(data_half_big, ignore_index = True)
	
    return data_half_low

## Decision tree and Random Forests related tools

def tree_to_code(tree, feature_names):
    
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    print("def tree({}):".format(", ".join(feature_names)))

    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            print ("{}if {} <= {}:".format(indent, name, threshold))
            recurse(tree_.children_left[node], depth + 1)
            print ("{}else:  # if {} > {}".format(indent, name, threshold))
            recurse(tree_.children_right[node], depth + 1)
        else:
            print ("{}return {}".format(indent, tree_.value[node]))

    recurse(0, 1)

## Machine learning models tools

def save_context(thing, name, folder):
 
    # Save to file in the current working directory
    pkl_filename = "{}/{}".format(folder, name)  
    with open(pkl_filename, 'wb') as file:  
        pickle.dump(thing, file)
        
def load_context(name, folder):
 
    # Save to file in the current working directory
    pkl_filename = "{}/{}".format(folder, name)  
    # Load from file
    with open(pkl_filename, 'rb') as file:  
        thing = pickle.load(file)
    
    return thing
    
def save_model(model, test, name, folder, feature_to_predict):
    
    features    = test.columns[:32]
    Xtest       = test[features]
    Ytest       = test[feature_to_predict]
    
    # Save to file in the current working directory
    pkl_filename = "{}/{}".format(folder, name)  
    with open(pkl_filename, 'wb') as file:  
        pickle.dump(model, file)
    
    # Load from file
    with open(pkl_filename, 'rb') as file:  
        pickle_model = pickle.load(file)
    
    # Calculate the accuracy score and predict target values
    score = pickle_model.score(Xtest, Ytest)  
    print("Test score: {0:.2f} %".format(100 * score))  
    
def load_model(joblib_file, test, feature_to_predict, acc_opt=-1):
    
    if acc_opt == 0:
        features    = test.columns[:32]
        Xtest       = test[features]
        Ytest       = test['Gait_event']
            
        # Load from file
        joblib_model = joblib.load(joblib_file)
        
        # Calculate the accuracy and predictions
        score = joblib_model.score(Xtest, Ytest)  
        print("Test score: {0:.2f} %".format(100 * score))
        
        return joblib_model

    else:
        joblib_model = joblib.load(joblib_file)
        return joblib_model

# Graphics and representation

## Console representation

def console_logger(list_to_print, sep_character='*', sep_elements='+'):

    print("{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}".format(sep_character))

    for index, element in enumerate(list_to_print):
        
        print("{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}".format(sep_elements))

        if type(element) == type([]):
            print('[')
            for subindex, subelement in enumerate(element):
                
                if type(subelement) == type([]):
                    print("\tindex:{}, value: sublist".format(subindex))
                    console_logger(subelement, '___')
                else:
                    print("\tindex: {}, value: {}".format(subindex, subelement))
        
            print(']')
        elif type(element) == type({}):
            print('{')
        else:    
            print("[{}] ==> {}".format(index, element))

    print("{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}{0}".format(sep_character))


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    # Code from: https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

## Confusion matrix graphics 

def get_new_fig(fn, figsize=[9,9]):
    """ Init graphics """
    fig1 = plt.figure(fn, figsize)
    ax1 = fig1.gca()   #Get Current Axis
    ax1.cla() # clear existing plot
    return fig1, ax1

def configcell_text_and_colors(array_df, lin, col, oText, facecolors, posi, fz, fmt, show_null_values=0):
    """
      config cell text and colors
      and return text elements to add and to dell
      @TODO: use fmt
    """
    text_add = []; text_del = [];
    cell_val = array_df[lin][col]
    tot_all = array_df[-1][-1]
    per = (float(cell_val) / tot_all) * 100
    curr_column = array_df[:,col]
    ccl = len(curr_column)

    #last line  and/or last column
    if(col == (ccl - 1)) or (lin == (ccl - 1)):
        #tots and percents
        if(cell_val != 0):
            if(col == ccl - 1) and (lin == ccl - 1):
                tot_rig = 0
                for i in range(array_df.shape[0] - 1):
                    tot_rig += array_df[i][i]
                per_ok = (float(tot_rig) / cell_val) * 100
            elif(col == ccl - 1):
                tot_rig = array_df[lin][lin]
                per_ok = (float(tot_rig) / cell_val) * 100
            elif(lin == ccl - 1):
                tot_rig = array_df[col][col]
                per_ok = (float(tot_rig) / cell_val) * 100
            per_err = 100 - per_ok
        else:
            per_ok = per_err = 0

        per_ok_s = ['%.2f%%'%(per_ok), '100%'] [per_ok == 100]

        #text to DEL
        text_del.append(oText)

        #text to ADD
        font_prop = fm.FontProperties(weight='bold', size=fz)
        text_kwargs = dict(color='w', ha="center", va="center", gid='sum', fontproperties=font_prop)
        lis_txt = ['%d'%(cell_val), per_ok_s, '%.2f%%'%(per_err)]
        lis_kwa = [text_kwargs]
        dic = text_kwargs.copy(); dic['color'] = 'g'; lis_kwa.append(dic);
        dic = text_kwargs.copy(); dic['color'] = 'r'; lis_kwa.append(dic);
        lis_pos = [(oText._x, oText._y-0.3), (oText._x, oText._y), (oText._x, oText._y+0.3)]
        for i in range(len(lis_txt)):
            newText = dict(x=lis_pos[i][0], y=lis_pos[i][1], text=lis_txt[i], kw=lis_kwa[i])
            text_add.append(newText)

        #set background color for sum cells (last line and last column)
        carr = [0.27, 0.30, 0.27, 1.0]
        if(col == ccl - 1) and (lin == ccl - 1):
            carr = [0.17, 0.20, 0.17, 1.0]
        facecolors[posi] = carr

    else:
        if(per > 0):
            txt = '%s\n%.2f%%' %(cell_val, per)
        else:
            if(show_null_values == 0):
                txt = ''
            elif(show_null_values == 1):
                txt = '0'
            else:
                txt = '0\n0.0%'
        oText.set_text(txt)

        #main diagonal
        if(col == lin):
            #set color of the textin the diagonal to white
            oText.set_color('w')
            # set background color in the diagonal to blue
            facecolors[posi] = [0.35, 0.8, 0.55, 1.0]
        else:
            oText.set_color('r')

    return text_add, text_del

def insert_totals(df_cm):
    """ insert total column and line (the last ones) """
    sum_col = []
    for c in df_cm.columns:
        sum_col.append( df_cm[c].sum() )
    sum_lin = []
    for item_line in df_cm.iterrows():
        sum_lin.append( item_line[1].sum() )
    df_cm['sum_lin'] = sum_lin
    sum_col.append(np.sum(sum_lin))
    df_cm.loc['sum_col'] = sum_col

def pretty_plot_confusion_matrix(df_cm, annot=True, cmap="Oranges", fmt='.2f', fz=11,
      lw=0.5, cbar=False, figsize=[8,8], show_null_values=0, pred_val_axis='y', save_route=None):
    """
      print conf matrix with default layout (like matlab)
      params:
        df_cm          dataframe (pandas) without totals
        annot          print text in each cell
        cmap           Oranges,Oranges_r,YlGnBu,Blues,RdBu, ... see:
        fz             fontsize
        lw             linewidth
        pred_val_axis  where to show the prediction values (x or y axis)
                        'col' or 'x': show predicted values in columns (x axis) instead lines
                        'lin' or 'y': show predicted values in lines   (y axis)
    """
    if(pred_val_axis in ('col', 'x')):
        xlbl = 'Predicted'
        ylbl = 'Actual'
    else:
        xlbl = 'Actual'
        ylbl = 'Predicted'
        df_cm = df_cm.T

    # create "Total" column
    insert_totals(df_cm)

    #this is for print allways in the same window
    fig, ax1 = get_new_fig('Conf matrix default', figsize)

    #thanks for seaborn
    ax = sn.heatmap(df_cm, annot=annot, annot_kws={"size": fz}, linewidths=lw, ax=ax1,
                    cbar=cbar, cmap=cmap, linecolor='w', fmt=fmt)

    #set ticklabels rotation
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 45, fontsize = 10)
    ax.set_yticklabels(ax.get_yticklabels(), rotation = 25, fontsize = 10)

    # Turn off all the ticks
    for t in ax.xaxis.get_major_ticks():
        t.tick1line.set_visible(False)
        t.tick2line.set_visible(False)
    for t in ax.yaxis.get_major_ticks():
        t.tick1line.set_visible(False)
        t.tick2line.set_visible(False)

    #face colors list
    quadmesh = ax.findobj(QuadMesh)[0]
    facecolors = quadmesh.get_facecolors()

    #iter in text elements
    array_df = np.array( df_cm.to_records(index=False).tolist() )
    text_add = []; text_del = [];
    posi = -1 #from left to right, bottom to top.
    for t in ax.collections[0].axes.texts: #ax.texts:
        pos = np.array( t.get_position()) - [0.5,0.5]
        lin = int(pos[1]); col = int(pos[0]);
        posi += 1

        #set text
        txt_res = configcell_text_and_colors(array_df, lin, col, t, facecolors, posi, fz, fmt, show_null_values)

        text_add.extend(txt_res[0])
        text_del.extend(txt_res[1])

    #remove the old ones
    for item in text_del:
        item.remove()
    #append the new ones
    for item in text_add:
        ax.text(item['x'], item['y'], item['text'], **item['kw'])

    #titles and legends
    ax.set_title('Confusion matrix')
    ax.set_xlabel(xlbl)
    ax.set_ylabel(ylbl)
    
    plt.tight_layout()  #set layout slim
    
    if save_route != None:
        plt.savefig(save_route)
    else: 
        plt.show()

def plot_confusion_matrix_from_data(y_test, predictions, columns=None, annot=True, cmap="Oranges",
      fmt='.2f', fz=11, lw=0.5, cbar=False, figsize=[8,8], show_null_values=0, pred_val_axis='lin'):
    """
        plot confusion matrix function with y_test (actual values) and predictions (predic),
        whitout a confusion matrix yet
    """
    from sklearn.metrics import confusion_matrix

    #data
    if(not columns):
        #labels axis integer:
        ##columns = range(1, len(np.unique(y_test))+1)
        #labels axis string:
        from string import ascii_uppercase
        columns = ['class %s' %(i) for i in list(ascii_uppercase)[0:len(np.unique(y_test))]]

    confm = confusion_matrix(y_test, predictions)
    cmap = 'Oranges';
    fz = 11;
    figsize=[9,9];
    show_null_values = 2
    df_cm = DataFrame(confm, index=columns, columns=columns)
    pretty_plot_confusion_matrix(df_cm, fz=fz, cmap=cmap, figsize=figsize, show_null_values=show_null_values, pred_val_axis=pred_val_axis)

# Data Structures tools

def binarySearch(alist, item):
    # Code from https://stackoverflow.com/questions/34420006/binary-search-python-3-5
    first = 0
    last = len(alist)-1
    found = False
    
    while first<=last and not found:
        midpoint = (first + last)//2
        if alist[midpoint] == item:
            found = True
        else:
            if item < alist[midpoint]:
                last = midpoint-1
            else:
                first = midpoint+1

    return found, midpoint

# System tools

def ls(ruta = getcwd()):
    # Code from https://es.stackoverflow.com/questions/24278/
    return [arch.name for arch in scandir(ruta) if arch.is_file()]

def read_json_file(route):
    with open(route) as json_file:
        json_file_readt = json.load(json_file)
    
    return json_file_readt

def write_list_to_file(list_to_write, output_file):
    file = open(output_file, 'w')
        
    for element in list_to_write:
        file.write("'{}',".format(element))

    file.close()

def mean(list_input):
    aggregation = functools.reduce(sum_funct, list_input, 0)

    return aggregation / float(len(list_input))

def variance(list_input):
    m = mean(list_input)
    v = functools.reduce(sum_funct, map(functools.partial(variance_funct, m=m), list_input))
    
    return v / float(len(list_input))

def standard_desviation(list_input):
    return math.sqrt(variance(list_input))

def list_to_num_dict(list_elements):

    dictionary = {}
    
    for element in list_elements:
        try:
            element = int(element)
            dictionary[element] = element
        except ValueError:
            dictionary[element] = len(dictionary)
            
            
    return dictionary


