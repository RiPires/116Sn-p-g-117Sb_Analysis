Descrição dos diferentes passos da análise dos dados da experiência:

    0. Estrutura da análise;
    1. Análise das espessuras dos alvos;
    2. Calibração dos detetores em energia;
    3. Caracterização do fundo dos detetores;
    4. Caracterização da eficiẽncia dos detetores;
    5. Curvas de acomulação;
    6. Cálculo das secções eficazes;

0. Estrutura da análise

        A análise está dividida em três pastas: CNA, CTN e DetSim.

        Na pasta CNA encontram-se todos os dados recolhidos em Sevilha, bem como a respetiva análise.
    Na pasta CTN encontram-se todos os dados recolhidos em Sacavém, bem como a respetiva análise.
    Na pasta DetSim encontram-se todas as simulações realizadas em Geant4, maioritariamente usadas para
    caracterizar a resposta em eficiência dos detetores utilizados.

    * CNA

            Aqui temos três pastas: Activations, Calibrations e Scripts-CNA.

            Na pasta Activations encontram-se os dados recolhidos durante a irradiação das amostras e a medida
        do decaimento. Para além dos dados "raw", contram-se também alguns ficheiros já processados - nomeadamente
        depois de realizara subtração do fundo.

            Na pasta Calibrations encontram-se os dados recolhidos durante as runs de calibração do sistema de aquisição.
        Estão divididos por detetor. Existem as runs onde se utilizaram as fontes radioativas certificadas , para realizar
        a avaliação da eficiência de medição em CalibrationRuns_PosExp. Existe também o ficheiro Detectors_E-calib.xlsx
        onde foi feita a calibração canal-energia dos detetores, bem como a avaliação da sua resolução energética.
        Para cada um dos detetores, existe ainda uma pasta Background, onde se encontram os dados recolhidos para
        avaliação do fundo da sala, que são posteriormente usados para processar dados raw.

            Na pasta Scripts-CNA encontram-se rotinas Python para realizar diferentes operações de visualização e processamento dos dados.
        Dentro, em include, estão escritas funções mais genéricas (Plot, Read, etc.) que podem ser utilizadas por outras mais específicas.
    
    * CTN

            Na pasta CTN encontra-se uma estrutura idêntica à da pasta CNA, com ficheiros equivalentes, mas adaptados
        aos dados recolhidos em Sacavém;

        * DetSim

            Nesta pasta são realizadas todas as simulações Geant4 dos detetores utilizados, nas dferentes circunstâncias,
        com o objetivo final de determinar as efeciências de medição dos fotões de interesse durante a medida do decaimento.

            Dentro, encontram-se 3 diretórios: 117Sb_Source, CalibRuns e Effs_MonoE. Em CalibRuns, separado por detetor,
        são realziadas simulações das situações em que calibrou cada detetor. Em 117Sb_Source realizam-se as simulações do
        cenário de medida do decaimento após uma ativação, também separado por detetor.


1. Análise das espessuras dos alvos

        Dentro de cada uma das pastas CNA e CTN encontram-se ficheiros onde é feita a avaliação das espessuras dos alvos
    utilizados em cada laboratório. As espessuras nominais determinadas em cada caso são posteriormente utilizadas na simulação
    da respetiva irradiação para efeitos da determinação da eficiência de medição.

2. Calibração dos detetores em energia

        A calibração dos multicanais em energia é feita numa folha de cálculo para cada laboratório.
    O processo começa em identificar, na literatura, as emissões (raios-X e gamma) de cada uma das fontes radioativas certificadas
    que foram usadas nas medidas de calibração. Depois, através de scripts Python, visualizam-se os espetros crus para estabelecer
    a relação entre a energia de cada foto-pico e o canal em que este aparece no espetro. É aplicada uma regressão linear
    que estabelece a relação canal-energia para cada detetor.

3. Caracterização do fundo (background)

        As medidas de fundo foram realizadas, à semelhança das medidas do decaimento, em modo de registar espetros em períodos fixos
    durante cerca de 24h. O script PlotBG permite visualizar cada espetro de fundo individualmente ou, recorrendo ao script MergeData
    visualizar o fundo acomulado ao longo de toda a medida.

        O script BgRemove permite realizar a subtração do fundo a outros espetros. O processo passa por determinar a taxa de fundo,
    em cada canal, usando o tempo total de medida do fundo e o espetro de fundo acomulado, e subtrair essa taxa de fundo, canal a canal,
    à taxa de contagens de um determinado ficheiro. Para recuperar o número de contagens, a taxa, já com o fundo subtraído, é multiplicada
    pelo tempo de medida desse ficheiro. É possível visualizar as três componentes (ficheiro raw, fundo, e fundo subtraído).
    É possivel escrever novos ficheiros já com o fundo substraido. Esta operação foi realizada para os ficheiros de calibração e para
    os ficheiros de medida do decaimento pós ativação. Em cada caso, junto dos dados originais, há pastas "BgRemoved" onde se encontram 
    os dados processados depois de subtrair o fundo.

4. Caracterização da eficiência

        A caracterização da eficiência divide-se em duas etapas: 1) durante as calibrações; 2) durante o decaimento pós ativação.

        Para determinar a eficiência de deteção às energias de interesse no decaímento 117Sb estamos limitados a utilizar as simulações.
    No entanto, começamos por avaliar as eficiências nas runs de calibração de forma a confirmar a fiabilidade do ambiente de simulação.
    Nas medidas de calibração, podemos comparar eficiências medidas experimentalmente, com eficiências extraidas das simulações.

        Começando pelo cálculo das eficiências experimentais, o potnto de partida é determinar o número total de decaímentos que ocorreram
    durante as medidas de calibração, para cada fonte. Essas contas encontram-se no ficheiro SourceActivity na pasta Calibrations.
    Utilizando os valores de referência de atividade das fontes à data em que foram certificadas, determina-se a atividade das fontes na
    altura da medida e calcula-se o número de decaimentos. Esse número será usado como denominador no cálculo das eficiências experimentais.
    Os numeradores vêm de, em cada foto-pico nos espetros de calibração adquiridos com as diferentes fontes radioativas, determinar o número
    total de contagens. Obtemos assim diferentes "curvas" de eficiência, correspondentes a diferentes distâncias a que as medidas foram realizadas.

        Em paralelo, simula-se a resposta em eficiência dos detetores para cada uma destas distâncias e compara-se com os valores experimentais.

        Numa outra linha, simula-se o decaimento do 117Sb, nas condições em que as medidas pós ativação foram realizadas, por forma a calcular,
    as eficiências necessárias para o cálculo da secção-eficaz, para cada energia de interesse. As simulações são realizadas a duas distâncias
    que diferem de +- 2 mm (isto é o quanto conseguimos limitar a medida da distância de cada medição). Para cada energia de interesse, é feita
    uma média simples entre as eficiências às duas distãncias (scripts Effs117Sb) e o valor resultante é posteriormente usado no cálculo do 
    parâmetro necessário para a determinação da secção-eficaz.

5. Curvas de acomulação

        Este é o passo mais delicado do processo, em que se projetam as curvas de acomulação e se efetua um fit aos dados experimentais de medida
    do decaimento pós ativação para extrair o parâmetro N_Dirr (número de núcleo radioativos presentes no alvo no final da irradiação) essencial
    para o cálculo da secção eficaz. Este processo é centralizado nos scripts Plot_Accumulation, que requerem algumas funções em include/Fits.
    Um dos inputs para determinar N_Dirr são as eficiẽncias determinados no passo anterior.