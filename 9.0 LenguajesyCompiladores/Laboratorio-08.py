class Tabla:
    def __init__(self):
        """
        Initializes the parsing table M, mirroring the C++ constructor.
        The table M is a list of lists of strings.
        M[0] serves as the header row for symbols.
        M[i][0] (for i > 0) serves as the state number identifier.
        """
        self.M = [[" " for _ in range(18)] for _ in range(22)]

        self.M[0][1] == "switch"  , self.M[0][2] == "case" , self.M[0][3] == "break",
        self.M[0][4] == "(", self.M[0][5] == ")", self.M[0][6] == "{", self.M[0][7] == "}", 
        self.M[0][8] == "..", self.M[0][9] == ";", self.M[0][10] == ":", self.M[0][11] == "id", 
        self.M[0][12] == "num", self.M[0][13] == "$", self.M[0][14] == "S", self.M[0][15] == "A",
        self.M[0][16] == "B" , self.M[0][17] == "T"
        
        self.M[1][0] == "0"      ,self.M[1][1] == "d2" , self.M[1][2] == "d11"  ,self.M[1][3] == "r3" ,self.M[1][7] == "r5" , self.M[1][8] == "d18" ,self.M[1][10] == "r7" ,self.M[1][13] == "r3",self.M[1][14] == "1"
        self.M[2][0] == "1"      ,self.M[2][3] == "r2" ,self.M[2][13] == "accept"
        self.M[3][0] == "2"      ,self.M[3][4] == "d3" 
        self.M[4][0] == "3"      ,self.M[4][11] == "d4"
        self.M[5][0] == "4"      ,self.M[5][5] == "d5" 
        self.M[6][0] == "5"      ,self.M[6][6] == "d6" 
        self.M[7][0] == "6"      ,self.M[7][2] == "d11" ,self.M[7][7] == "d5" ,  self.M[7][16] == "7"
        self.M[8][0] == "7"      ,self.M[8][7] == "d8"
        self.M[9][0] == "8"      ,self.M[9][1] == "d2" ,self.M[9][3] == "r3" ,self.M[9][13] == "r3", self.M[9][14] == "9" , self.M[9][15] == "10"
        self.M[10][0] == "9"     ,self.M[10][3] == "r2" ,self.M[10][13] == "r2"
        self.M[11][0] == "10"    ,self.M[11][3] == "r1" , self.M[11][13] == "r1" 
        self.M[12][0] == "11"    ,self.M[12][12] == "d12"
        self.M[13][0] == "12"    ,self.M[13][8] == "d19",self.M[13][10] == "r7" , self.M[13][17] == "13"
        self.M[14][0] == "13"    ,self.M[14][10] =="d14"
        self.M[15][0] == "14"    ,self.M[15][1] == "d2" ,self.M[15][3] == "r3" ,self.M[15][13] == "r3", self.M[15][14] == "9", self.M[15][15] == "15"
        self.M[16][0] == "15"    ,self.M[16][3] == "d16" 
        self.M[17][0] == "16"    ,self.M[17][9] == "d17"
        self.M[18][0] == "17"    ,self.M[18][2] == "d11" ,self.M[18][7] == "r5"
        self.M[19][0] == "18"    ,self.M[19][7] == "r4"
        self.M[20][0] == "19"    ,self.M[20][12] == "d20"
        self.M[21][0] == "20"    ,self.M[21][10] == "r6" 


    def accion(self, xx_estado_str, ae_simbolo_entrada_str):
        col_idx = 0  
        for i in range(1, 17):  # M[0][1] to M[0][17]
            if self.M[0][i] == ae_simbolo_entrada_str:
                col_idx = i
                break
        row_idx = 0  
        for i in range(1, 21): # M[1][0] to M[21][0]
            if self.M[i][0] == xx_estado_str:
                row_idx = i
                break
        
        # If symbol or state was not found, or if an invalid index was derived
        if col_idx == 0 or row_idx == 0:
            return " "  # Return space, indicating an error or empty cell
        else:
            return self.M[row_idx][col_idx]

    def ir_a(self, xx_estado_str, tira_simbolo_str):
        """
        Alias for the accion method, as in the C++ code.
        char *Ir_a(char xx[PRO],char tira[PRO]){ return accion(xx,tira); }
        """
        return self.accion(xx_estado_str, tira_simbolo_str)
    
    
    