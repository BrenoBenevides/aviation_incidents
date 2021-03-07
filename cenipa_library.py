import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def card_chart(data,columns,number_cols=2):

    #dados
    df_total_acidentes = data.count()[0]
    df_aeronaves_env = data['aeronaves_envolvidas'].sum()
    df_categoria_mais = data.tipo_categoria.value_counts()
    df_status_acidentes = data.status.value_counts()

    texts = [("Total Acidentes",df_total_acidentes,"acidentes"),
             ("Aeronaves Envolvidas",df_aeronaves_env,"aeronaves"),
             ("Categoria c/ + acidentes",str(int((df_categoria_mais.values[0]*100)/df_total_acidentes))+"%",df_categoria_mais.index[0]),
             ("Status dos Acidentes",str(int((df_status_acidentes.values[0]*100)/df_total_acidentes))+"%",df_status_acidentes.index[0])
             ]

    #configurações
    facecolors = ["#000033"]
    fontcolors = ['white']

    #Plotagem
    number_rows = int(len(columns) / number_cols)
    text_index = 0

    fig, ax = plt.subplots(nrows=number_rows, ncols=number_cols, figsize=(15, 8))

    for x in range(number_rows):
        for y in range(number_cols):
            ax[x, y].grid(False)
            ax[x, y].tick_params(left=False, right=False, labelbottom=False, labelleft=False)
            ax[x, y].set_facecolor(facecolors[0])
            ax[x,y].text(0.5,0.9,texts[text_index][0],fontsize=24,ha='center',va='center',color="#A0A0A0",weight='bold') #Titulo
            ax[x, y].text(0.5, 0.55, texts[text_index][1], fontsize=80, ha='center', va='center', color="#FFFFFF",weight='bold') #Valor
            ax[x, y].text(0.5, 0.2, texts[text_index][2], fontsize=24, ha='center', va='center', color="#FFFFFF",weight='bold') #Descrição
            text_index += 1

    return st.pyplot(fig)

def get_month_name(number):
    months = {1:"Janeiro",2:"Fevereiro",3:"Março",4:"Abril",5:"Maio",6:"Junho",
              7:"Julho",8:"Agosto",9:"Setembro",10:"Outubro",11:"Novembro",12:"Dezembro"}
    return months[number]

def year_comparasion(this_year,last_year,column,by_column=None):

    if by_column is None:
        pct_change = int(this_year.shape[0] * 100 / last_year.shape[0] - 1)
        return str(pct_change) + "%"
    else:
        if this_year[column][0] == str:
            pct_change = this_year[column].count() *100 / last_year[column].count() - 1
            return pct_change
        else:
            pct_change = this_year[column].sum()  / last_year[column].sum()
            return pct_change

def bar_chart(data,column,kind="bar",is_datetime=None):

    if is_datetime is None:
        data_grp = data.groupby(column)[column].count()

    else:
        data_grp = data.groupby(data[column].dt.month)[column].count()
        data_grp.index = get_month_name(data_grp.index)

    fig,ax = plt.subplots(1,2,figsize=(16,8))

    ax[0,0].grid(False)
    ax[0,0].set_title("Titulo 1")
    ax[0,0].plot(data_grp.index,data_grp.values,kind=kind)

    ax[0, 1].grid(False)
    ax[0, 1].set_title("Titulo 1")
    ax[0, 1].plot(data_grp.index, data_grp.values, kind=kind)

    return st.pyplot(fig)


