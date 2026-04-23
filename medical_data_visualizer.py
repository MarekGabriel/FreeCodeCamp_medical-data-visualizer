import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
# Import the data from medical_examination.csv and assign it to the df variable.

df = pd.read_csv('https://raw.githubusercontent.com/freeCodeCamp/boilerplate-medical-data-visualizer/refs/heads/main/medical_examination.csv',
                 header = 0, index_col = 0)


# 2. 
# Add an overweight column to the data. To determine if a person is overweight, first calculate their BMI by dividing 
# their weight in kilograms by the square of their height in meters. If that value is > 25 then the person is overweight. 
# Use the value 0 for NOT overweight and the value 1 for overweight.

#df['BMI'] = df['weight'] / ((df['height'] / 100) ** 2)
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2) > 25) * 1


# 3
# Normalize data by making 0 always good and 1 always bad. If the value of cholesterol or gluc is 1, set the value to 0. 
# If the value is more than 1, set the value to 1.

#df['cholesterol'].unique()
#df['gluc'].unique()

#kolumna 'cholesterol' będzie boolean i będzie oznaczać przekroczenie normy, gdzie 0 - ok, 1 - źle
df['cholesterol'] = ~(df['cholesterol'] == 1) * 1
#kolumna 'gluc' będzie boolean i będzie oznaczać przekroczenie normy, gdzie 0 - ok, 1 - źle
df['gluc'] = ~(df['gluc'] == 1) * 1


# 4
# Draw the Categorical Plot in the draw_cat_plot function.

def draw_cat_plot():
    
    # 5
    # Create a DataFrame for the cat plot using pd.melt with values from cholesterol, gluc, smoke, alco, active, 
    # and overweight in the df_cat variable.

    #trzeba przerobić ramkę danych na tzw. format "long" dla rysowania wykresów kategorii tj. catplot() -> funkcja pandas.melt()
    ### .melt() to funkcja w Pythonie służąca do przekształcania struktury danych z formatu „szerokiego” (wide) na „długi” (long). 
    ### Przetapia ona wybrane kolumny na wiersze, co jest kluczowe do przygotowania danych pod analizę, grupowanie lub wizualizację 
    ### (np. w bibliotekach typu seaborn). Jest to operacja typu unpivot. Generalnie chcemy doprowadzić do tego, że na wykresie
    ### jednak z osi (np.x) będzie pokazywać właśnie kategorie (czyli nazwy kolumn z pierwotnej ramki danych przerobione na jedną 
    ### nową kolumnę (domyślnie variable).
    ### Składnia: pandas.melt(frame, id_vars=None, value_vars=None, var_name=None, value_name='value')
    ### Parametry funkcji to: 
    ###   frame - to po prostu dane wejściowe jako DataFrame
    ###   id_vars - kolumny, które mają zostać bez zmian tj. pozostaną dalej kolumnami
    ###   value_vars - kolumny, które mają zostać „przetopione” na wiersze (domyślnie wszystkie pozostałe)
    ###   var_name - nowa nazwa dla kolumny przechowującej stare nazwy kolumn (domyślnie: variable)
    ###   value_name - nowa nazwa dla kolumny przechowującej wartości (domyślnie: value)

    #format long ramki danych
    df_melted = pd.melt(df[['cholesterol','gluc','smoke','alco','active','overweight','cardio']], id_vars = ['cardio'])
    #sortuję ramkę alfabetycznie po values (czyli po cholesterol, gluc, etc.)
    df_melted.sort_values('variable', inplace = True)

    #temp result
    df_cat = df_melted
    
    #wykres na danych w formacie tzw. "long" dla catplot() (dlatego kind = 'count')
    #sns.catplot(x = 'variable', hue = 'value', col = 'cardio', kind = 'count', data = df_cat)

    # 6
    # Group and reformat the data in df_cat to split it by cardio. Show the counts of each feature. 
    # You will have to rename one of the columns for the catplot to work correctly.

    #grupowanie danych po variables i value (np. active, 0 lub active, 1, etc.) i po kolumnie cardio; zliczamy wystąpienia po kolumnie value
    #dopiero wtedy dostajemy liczności w każdej podgrupie i np.:
    #active=0,cardio=0 + active=0,cardio=1 + active=1,cardio=0 + active=1,cardio=1 = 70000 czyli liczba wszystkich pacjentów z df
    #i tak samo dla innych niż active cech będzie się to sumować do wszystkich pacjentów z pierwotnej ramki danych 70000
    df_cat_grouped = df_cat.groupby(['variable','value','cardio'])['value'].count().to_frame()
    #zmieniam nazwę licznika na 'total' (liczba pacjentów), bo domyślnie ustawia się 'value'
    df_cat_grouped.columns = ['total']
    #wynik grupowania dostarcza tzw. multiIndex, dlatego przerzucam go do kolumn
    df_cat_grouped.reset_index(inplace = True)

    #temp result
    df_cat = df_cat_grouped
    

    # 7
    # Convert the data into long format and create a chart that shows the value counts of the categorical features
    # using the following method provided by the seaborn library import: sns.catplot().

    #wykres na danych w formacie tzw. "long" dla catplot() (dlatego kind = 'count')
    #sns.catplot(x = 'variable', hue = 'value', col = 'cardio', kind = 'count', data = df_melted)
    
    ### seaborn.catplot() funkcja rysująca wykres kategorii
    ### Składnia: seaborn.catplot(x=None, y=None, hue=None, data=None, row=None, col=None, kind=string, color=None, palette=None)
    ### Parametry funkcji to: 
    ###   data - wejściowa ramka danych jako pandas.DataFrame w tzw. formacie "long"
    ###   x, y -  names of variables in data (pod jedną z nich podstawiamy właśnie kategorie "schowane" do nowej kolumny w wyniku pd.melt()
    ###   hue -  name of variable in data (atrybut, po którym rozróżnimy kolory serii, u nas wartości dla kolumn schowanych do variable)
    ###   row, col -  names of variables in data, optional. Są to kolumny, które zdeterminują podział wykresu na więcej niż jeden wierszowo
    ###   lub kolumnowo.
    ###   kind -  The kind of plot to draw. Options are: “strip”, “swarm”, “box”, “violin”, “boxen”, “point”, “bar”, or “count”.
    
    #wykres na danych w formacie tzw. "long" po grupowaniach (dlatego kind = 'bar')
    category_plot = sns.catplot(x = 'variable', y = 'total', hue = 'value', col = 'cardio', kind = 'bar', data = df_cat)
    #type(category_plot) --> seaborn.axisgrid.FacetGrid
    
    # 8
    # Get the figure for the output and store it in the fig variable.

    #Funkcja seaborn sns.catplot() zwraca obiekt typu FacetGrid, a nie bezpośrednio figurę z matplotlib.
    fig = category_plot.fig
    #type(fig) --> matplotlib.figure.Figure

    # 9
    # Do not modify the next two lines.
    fig.savefig('catplot.png')
    return fig


# 10
# Draw the Heat Map in the draw_heat_map function.

def draw_heat_map():
    
    # 11
    # Clean the data in the df_heat variable by filtering out the following patient segments that represent incorrect data:
    #   - diastolic pressure is higher than systolic (Keep the correct data with (df['ap_lo'] <= df['ap_hi']))
    #   - height is less than the 2.5th percentile (Keep the correct data with (df['height'] >= df['height'].quantile(0.025)))
    #   - height is more than the 97.5th percentile
    #   - weight is less than the 2.5th percentile
    #   - weight is more than the 97.5th percentile

    # a. diastolic pressure is higher than systolic (Keep the correct data with (df['ap_lo'] <= df['ap_hi']))
    #df.drop(df[~(df['ap_lo'] <= df['ap_hi'])].index, inplace = True)
    #creating a mask, so boolean values representing rows to be finally excluded
    condition1 = ~(df['ap_lo'] <= df['ap_hi'])
    
    # b. height is less than the 2.5th percentile (Keep the correct data with (df['height'] >= df['height'].quantile(0.025)))
    condition2 = ~(df['height'] >= df['height'].quantile(0.025))
    
    # c. height is more than the 97.5th percentile
    condition3 = df['height'] > df['height'].quantile(0.975)
    
    # d. weight is less than the 2.5th percentile
    condition4 = df['weight'] < df['weight'].quantile(0.025)
    
    # e. weight is more than the 97.5th percentile
    condition5 = df['weight'] > df['weight'].quantile(0.975)
    
    #df[condition1 | condition2 | condition3 | condition4 | condition5]

    # final result (rows with incorrect data excluded)
    df_heat = df.drop(df[condition1 | condition2 | condition3 | condition4 | condition5].index)
    #okazało się, że indeks 'id' powinien pojawić się jako pierwsza zmienna/kolumna w macierzy korelacji budowanej poniżej
    df_heat.reset_index(inplace = True)
    
    # 12
    # Calculate the correlation matrix and store it in the corr variable.
    
    ### Do wyznaczania macierzy korelacji w Pandas używa się metody DataFrame.corr() 
    ### Bierze ona wszystkie kolumny numeryczne z ramki danych, liczy korelacje między każdą parą i zwraca macierz (DataFrame).
    ### Można też wybrać metodę liczenia, tj. typ korelacji:
    ###   - df.corr(method="pearson")   # domyślna
    ###   - df.corr(method="spearman")  # dla zależności monotonicznych
    ###   - df.corr(method="kendall")   # bardziej odporna na odstające
    
    corr = df_heat.corr()

    
    # 13
    # Generate a mask for the upper triangle and store it in the mask variable.

    #ustalenie rozmiaru macierzy korelacji
    rozmiar = corr.shape
    #generowanie macierzy boolean (tylko True) o rozmiarze zgodnym z macierzą korelacji
    macierz = np.full(rozmiar, 1, dtype = bool)
    #pętla, która na wygenerowanej powyżej macierzy dolny jej "trójkąt" zamieni na False
    i = 1
    for wiersz in macierz:
        j = 1
        for kolumna in wiersz:
            if i > j:
                macierz[i - 1, j - 1] = False
            #print((i, j), kolumna, '\n')
            j += 1
        i += 1
    #macierz
    
    #final result
    mask = macierz


    # 14
    # Set up the matplotlib figure.

    #plt.figure(figsize=(12, 6))
    
    # przy użyciu plt.subplots() tworzę tło (figure) w zadanym rozmiarze pod wykres oraz definiuję jeden wykres w pozycji [0,0]
    # fig - zmienna, pod którą podstawiamy tło
    # ax - zmienna, pod którą podstawiamy wykres (osie); UWAGA - moglibyśmy zdefiniować ich więcej, wówczas ax byłby macierzą ndarray
    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (24, 12))
    #ax.set_xlabel('X')
    #ax.set_ylabel('Y')
    #ax.set_title('Tytuł')
    #ax.legend([]);

    
    # 15
    # Plot the correlation matrix using the method provided by the seaborn library import: sns.heatmap().

    ### seaborn.heatmap() funkcja rysująca tzw. heatmapę
    ### Składnia: seaborn.heatmap(data=DataFrame, annot=None, fmt=None, cmap=None, cbar=None, vmin=None, vmax=None, square=None, mask=None)
    ### Parametry funkcji to: 
    ###   data - wejściowa ramka danych, ale uwaga musi być w postaci tablicy dwudzielnej (idealna do tego jest macierz korelacji, względnie
    ###     z danej ramki danych funkcją .pivot() przygotowuje się taką tablicę dwudzielną
    ###   annot - ustawione na True wyświetli wartości w komórkach
    ###   fmt - ustawia format wyświetlanych wartości, np. .1f to jedna cyfra po przecinku
    ###   cmap - różne style kolorów
    ###   cbar - ustawione na True pozwoli wyświetlić legendę kolorów obok wykresu
    ###   vmin, vmax - zakres wartości od-do dla zmiennej prezentowanej w komórkach
    ###   square - ustawione na True pozwoli wyświetlić komórki wewnątrz heatmapy jako kwadraty
    ###   mask - to macierz (ndarray o tym samym rozmiarze co data) wartości True/False jako sposób na ukrycie wybranych komórek w heatmapie
    
    ax = sns.heatmap(data = corr, fmt = '.1f', annot = True, cbar = True, mask = mask, square = True)


    # 16
    # Do not modify the next two lines.
    fig.savefig('heatmap.png')
    return fig
