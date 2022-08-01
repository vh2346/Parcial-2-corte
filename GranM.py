# -*- coding: utf-8 -*-

# =============================================================================
# Se importa las librerias de tkinter(Interfaz) y numpy (Algoritmo)
# =============================================================================

from curses import COLOR_CYAN
from msilib.schema import Font
from tkinter import *
from tkinter import ttk
import tkinter as tk
from turtle import color
from matplotlib.font_manager import FontProperties

import sympy as sym

import numpy as np

# =============================================================================
# Creación Ventana Principal
# =============================================================================
raiz=tk.Tk()
raiz.title("Método de la Gran M")
raiz.geometry("700x500")

# =============================================================================
# Creación de Frames Utilizados en la ejecución de la aplicación
# =============================================================================

w=700
h=500

frame1=Frame(raiz, width=w, height=h)
frame1.pack(fill='both', expand=1)
frame2=Frame(raiz, width=w, height=h)
frame3=Frame(raiz, width=w, height=h)
frame4=Frame(raiz, width=w, height=h)
newFrame=Frame(raiz, width=w, height=h)
finalFrame=Frame(raiz, width=w, height=h)

# =============================================================================
#   Método principal de Ejecución del programa
# =============================================================================
def main():
    frm1()
    
    
# =============================================================================
#   Creación de elementos del Frame 1 (Ventana Inicial)
# =============================================================================
def frm1():
    
    Lbl1=tk.Label(frame1, text="Metodo de la Gran M")
    Lbl1.config(font=("Helvetica",14))
    Lbl1.grid(pady=5,row=0,column=0, columnspan=2)
    
    Lblm=tk.Label(frame1, text="", height=7)
    Lblm.grid(pady=5,row=1,column=1)
    
    Lbl1_=tk.Label(frame1, text="Tipo de Optimización:")
    Lbl1_.config(font=("Helvetica",12))
    Lbl1_.grid(pady=5,row=2,column=0)
    
    des=ttk.Combobox(frame1, width=30)
    des['values']=('Maximizar', 'Minimizar')
    des.grid(pady=5,row=2, column=1)
    
    Lbl1_1=tk.Label(frame1, text="Numero de Variables")
    Lbl1_1.config(font=("Helvetica",12))
    Lbl1_1.grid(pady=5,row=3,column=0)
        
    Txt1=tk.Text(frame1, height=1.5, width=30)
    Txt1.config(font=("Helvetica",12))
    Txt1.grid(pady=5,row=3,column=1)
        
    Lbl1_2=tk.Label(frame1, text="Numero de Restricciones")
    Lbl1_2.config(font=("Helvetica",12))
    Lbl1_2.grid(pady=1,row=4,column=0)
        
    Txt1_1=tk.Text(frame1, height=1.5, width=30)
    Txt1_1.config(font=("Helvetica",12))
    Txt1_1.grid(pady=1,row=4,column=1)

    Btn1=tk.Button(frame1, text="Aceptar", width=60,command=lambda: frm2(des.get(),Txt1.get("1.0","end"),Txt1_1.get("1.0","end")))
    Btn1.grid(padx=1,pady=5,row=5,column=0, columnspan=2)

# =============================================================================
# Creación de elementos del frame 2 (Ventana para ingresar Coeficientes)
# =============================================================================
def frm2(tipo, N_Var, N_Res):
    
    frame1.pack_forget()
    frame2.pack()
    
    N_Var=int(N_Var)
    N_Res=int(N_Res)
    
    Lbl2=tk.Label(frame2, text="Metodo de la Gran M")
    Lbl2.config(font=("Helvetica",14))
    Lbl2.grid(pady=5,row=0,column=0, columnspan=int(N_Var)+1)

    Lbl2_1=tk.Label(frame2, text="Función Objetivo")
    Lbl2_1.config(font=("Helvetica",11))
    Lbl2_1.grid(pady=5,row=1,column=0)
    
    Fun_Obj={}
    
    for i in range (int(N_Var)):
                
        Fun_Obj.setdefault(i,tk.Text(frame2, height=1, width=6))
        Fun_Obj.setdefault(i).config(font=("Helvetica",11))
        Fun_Obj.setdefault(i).grid(pady=5,row=1,column=i+1)
        
    Lbl2_2=tk.Label(frame2, text="Restricciones:")
    Lbl2_2.config(font=("Helvetica",11))
    Lbl2_2.grid(pady=5,row=2,column=0)
    
    Rest={}
    cont=0
    for i in range (int(N_Res)):        
        for j in range(int (N_Var)):                    
            Txt3=tk.Text(frame2, height=1, width=6)
            Txt3.config(font=("Helvetica",11))
            Txt3.grid(pady=5,row=i+3,column=j+1)
            Rest.setdefault(cont, Txt3)
            cont+=1
        
        des=ttk.Combobox(frame2, width=3)
        des['values']=('>=', '=', '<=')
        des.grid(pady=5,row=i+3, column=int(N_Var)+1)
        Rest.setdefault('r'+str(i),des)
        
        Txt4_i=tk.Text(frame2, height=1, width=6)
        Txt4_i.config(font=("Helvetica",11))
        Txt4_i.grid(pady=5,row=i+3,column=int(N_Var)+2)
        Rest.setdefault('b'+str(i),Txt4_i)
    
    paso=1
    
    Btn2=tk.Button(frame2, text="Continuar", width=60, 
                   command=lambda: ejecutar(tipo, Fun_Obj, Rest, N_Var, N_Res,paso))
    Btn2.grid(padx=1,pady=5,row=int(N_Res)+3,column=0, columnspan=int(N_Var)+1)
    
# =============================================================================
# Toma los elementos de la ventana de los coeficientes y los asigna a las matrices
# y vectores correspondientes para la primera iteración    
# =============================================================================
def transformar(tipo, Fun_Obj, Rest, N_Var, N_Res):
    Coef=[]
    Hol=[]
    Art=[]
    b=[]
    cont=0
    for i in range(N_Res):
        nx=[]        
        for j in range(N_Var):
            n=Rest.get(cont).get("1.0","end")
            nx.append(float(n))
            cont+=1        
        Coef.append(nx)
            
        n=Rest.get('b'+str(i)).get("1.0","end")
        b.append(float(n))
        
        r=Rest.get('r'+str(i)).get()
        if(r == '>='):
            a=np.zeros(N_Res, dtype=int) 
            h=np.zeros(N_Res, dtype=int)
            a[i]=1
            h[i]=-1
            Art.append(a)
            Hol.append(h)
            
        if(r == '='):
            a=np.zeros(N_Res, dtype=int)
            a[i]=1
            Art.append(a)
            
        if(r == '<='):
            h=np.zeros(N_Res, dtype=int)
            h[i]=1
            Hol.append(h)
          
    b=np.array(b)
      
    matriz=np.concatenate((Coef,np.transpose(np.concatenate((Hol, Art),axis=0)),b.reshape(N_Res,1)),axis=1)
    
    Co=np.zeros(matriz.shape[1]-1, dtype=float)
    
    for i in range(matriz.shape[1]-1):
        if(i<N_Var):
            Co[i]=Fun_Obj.get(i).get("1.0", "end")
    
        if(i>((N_Var-1)+np.array(Hol).shape[0])):
            if(tipo=='Maximizar'):
                Co[i]=-1     
            if(tipo=='Minimizar'):
                Co[i]=1
    return [matriz, Co]
  
# =============================================================================
# Prepara los coeficientes para la primera iteración, agregando variables artificiales 
# y de holgura, organizandolas en el orden de una matriz de identidad   
# =============================================================================
    
def ejecutar(tipo, Fun_Obj, Rest, N_Var, N_Res, paso):
    if(paso==1):
        """ 
       Toma los coeficientes ingresados, separando coeficientes de la función
       objetivo y de las restricciones            
        """
        
        matriz=transformar(tipo, Fun_Obj, Rest, N_Var, N_Res)
        Coef=np.array(matriz[1])
        matriz=np.array(matriz[0])
        
        Var=[]
        h=1
        a=1
        """ 
        Agrega variables de holgura y artificiales, de acuerdo a 
        las restricciones ingresadas
        """
        for i in range(len(Coef)):
            if(i<N_Var):
                Var.append('X'+str(i+1))
            if(i>=N_Var):
                if(Coef[i]==0):
                    Var.append('H'+str(h))
                    h+=1
                if(Coef[i]==1 or Coef[i]==-1):
                    Var.append('A'+str(a))
                    a+=1
        """ 
        Agrega los coeficientes de las restricciones, junto con las variables de 
        holgura y artificiales a una sola matriz para comenzar a aplicar el método
        """
        cont=0
        for i in range(matriz.shape[1]-2,N_Var-1, -1):
            if(cont<matriz.shape[0]):
                fila=(matriz.shape[0]-1)-cont
                if(matriz[fila][i]!=1):
                    for j in range(N_Var, matriz.shape[1]-1):
                        if (matriz[fila][j]==1):
                            matriz=np.concatenate((matriz,np.array(matriz[:,j]).reshape(matriz.shape[0],1)),
                                                  axis=1)
                            Coef=np.append(Coef, Coef[j])
                            Var=np.append(Var, Var[j])
                            
                            matriz[:,j]=matriz[:,i]
                            Coef[j]=Coef[i]
                            Var[j]=Var[i]
                            
                            matriz[:,i]=matriz[:,matriz.shape[1]-1]
                            Coef[i]=Coef[Coef.shape[0]-1]
                            Var[i]=Var[Var.shape[0]-1]
                            
                            matriz=np.delete(matriz,matriz.shape[1]-1,axis=1)
                            Coef=np.delete(Coef, Coef.shape[0]-1)
                            Var=np.delete(Var, Var.shape[0]-1)
                            
                            break
                cont+=1
        """ Toma los coeficientes para la base """
        base=Coef[Coef.shape[0]-N_Res: Coef.shape[0]]
        
        """ Toma las variables para la base """
        V_Base=Var[len(Var)-matriz.shape[0]:len(Var)]
        
        """ Calcula las filas Zj y Cj-Zj para la primera iteración """
        Zj=np.zeros(matriz.shape[1], dtype=float)
        
        for i in range(N_Res):
            n=base[i]*matriz[i]
            Zj=n+Zj
            
        Cj_Zj=Coef-Zj[0:len(Zj)-1]
        
    """ Imprime la primera tabla """
 
    imprimir(Coef, Var, V_Base,base, matriz, Zj, Cj_Zj, tipo, paso, True)
    paso+=1
    
# =============================================================================
# Función utilizada para realizar la impresión de cada uno de los tableros
# correspondientes a los pasos de solución
# =============================================================================
def imprimir(Coef, Var,V_Base,base, matriz, Zj, Cj_Zj, tipo,paso, fase):
   
    Labl=['Cj', 'VB']
    if(fase):
        frame2.pack_forget()
        frame3.pack_forget()
        
        sym.init_printing(use_unicode=False, wrap_line=True)
        
        M=sym.Symbol('M')
        V=[]
        for i in range(len(base)):
            if ('A' in V_Base[i]):
                V.append(M*int('%g'%(base[i])))
            else:
                try:
                    V.append(int('%g'%(base[i])))
                except:
                    V.append(float('%g'%(base[i])))
        
        m=[]
        for i in range(matriz.shape[0]):
           try:
               m.append([int('%g'% n) for n in matriz[i]])
           except:
               m.append(matriz[i])
        n=np.array(m)*np.array(V)[:,np.newaxis]
        Z=n.sum(axis=0)
        
        C=[]
        for i in range(len(Coef)):
            if('A' in Var[i]):
                C.append(M*Coef[i])
            else:
                C.append(Coef[i])
        try:
            CZ=np.array([int('%g'% n) for n in C]-(Z[0:len(Z)-1]))
        except:
            CZ=np.array(C-(Z[0:len(Z)-1]))
        
        if (paso>1):
            Lbl3=tk.Label(frame4, text="Metodo de la Gran M Paso "+str(paso))
        else:
            Lbl3=tk.Label(frame3, text="Metodo de la Gran M Paso "+str(paso))
        Lbl3.config(font=("Helvetica",14))
        Lbl3.grid(pady=5,row=0,column=0, columnspan=matriz.shape[1]+2)
        
        Labl=np.concatenate((Labl, V_Base,['Zj','Cj-Zj']))
        Var=np.append(Var,'b')
              
        for i in range(matriz.shape[0]+4):
            for j in range(matriz.shape[1]+1):
                if (paso>1):
                    Txt3_1=tk.Entry(frame4, width=6)
                else:
                    Txt3_1=tk.Entry(frame3, width=6)
                Txt3_1.config(font=("Helvetica",12))
                Txt3_1.grid(row=i+1,column=j)
                
                if(i>1 and j>0 and j<(matriz.shape[1]+1)):
                    if(i<(matriz.shape[0]+2)):
                        Txt3_1.insert(0,'%g'%(round(matriz[i-2][j-1], 2)))
                    if(i==(matriz.shape[0]+2)):  
                        Txt3_1.insert(0,Z[j-1])
                    if(i==(matriz.shape[0]+3) and j<matriz.shape[1]):
                        Txt3_1.insert(0,CZ[j-1])
                if(j==0):
                    Txt3_1.insert(0,Labl[i])
                if(i==1 and j>0):
                    Txt3_1.insert(0,Var[j-1])
                if(i==0 and j>0 and j<(matriz.shape[1])):
                    if('A' in Var[j-1]):
                        if(Coef[j-1]==1):    
                            Txt3_1.insert(0,'M')
                        if(Coef[j-1]==-1):
                            Txt3_1.insert(0,'-M')
                    else:
                        Txt3_1.insert(0,'%g'%(Coef[j-1]))
        if (paso>1):
            Btn2=tk.Button(frame4, text="Continuar", width=60, command=lambda: calcular(Coef, Var,V_Base,base, matriz, Zj, Cj_Zj, tipo, paso))
        else:
            Btn2=tk.Button(frame3, text="Continuar", width=60, command=lambda: calcular(Coef, Var,V_Base,base, matriz, Zj, Cj_Zj, tipo, paso))
        Btn2.grid(padx=1,pady=5,row=matriz.shape[0]+5,column=0, columnspan=matriz.shape[1])
        
        Aux=Zj_M(base, V_Base)
        
        C=Zj_M(Coef, Var)
        
        Zj, Cj_Zj = CjZj(matriz, Aux, C)
        
        Fil, Col=Pivote(matriz, Cj_Zj, V_Base, tipo)
        
        if (paso>1):
            Lbl3_1=tk.Label(frame4, text='V. Ent: '+Var[Col])
            Lbl3_2=tk.Label(frame4, text='V. Sal: '+V_Base[Fil])
            Lbl3_3=tk.Label(frame4, text='Pivote: '+'%g'%(matriz[Fil][Col]))
        else:
        
            Lbl3_1=tk.Label(frame3, text='V. Ent: '+Var[Col])
            Lbl3_2=tk.Label(frame3, text='V. Sal: '+V_Base[Fil])
            Lbl3_3=tk.Label(frame3, text='Pivote: '+'%g'%(matriz[Fil][Col]))
            
        Lbl3_1.config(font=("Helvetica",12))
        Lbl3_1.grid(pady=5,row=matriz.shape[0]+6,column=0, columnspan=3)
        
        
        Lbl3_2.config(font=("Helvetica",12))
        Lbl3_2.grid(pady=5,row=matriz.shape[0]+7,column=0, columnspan=3)
        
        
        Lbl3_3.config(font=("Helvetica",12))
        Lbl3_3.grid(pady=5,row=matriz.shape[0]+8,column=0, columnspan=3)
        if (paso>1):
            frame4.pack() 
        else:
            frame3.pack()
        
    elif(terminar(tipo, Cj_Zj)==False):
        frame3.pack_forget()
        frame4.pack_forget()
        
        Lbl3=tk.Label(newFrame, text="Metodo de la Gran M Paso "+str(paso))
        Lbl3.config(font=("Helvetica",14))
        Lbl3.grid(pady=5,row=0,column=0, columnspan=matriz.shape[1]+2)
        
        Labl=np.concatenate((Labl, V_Base,['Zj','Cj-Zj']))
        for i in range(matriz.shape[0]+4):
            for j in range(matriz.shape[1]+1):
                Txt3_1=tk.Entry(newFrame, width=6)
                Txt3_1.config(font=("Helvetica",12))
                Txt3_1.grid(row=i+1,column=j)
                
                if(i>1 and j>0 and j<(matriz.shape[1]+1)):
                    if(i<(matriz.shape[0]+2)):
                        Txt3_1.insert(0,'%g'%(round(matriz[i-2][j-1], 2)))
                    if(i==(matriz.shape[0]+2)):            
                        Txt3_1.insert(0,'%g'%(round(Zj[j-1],2)))
                    if(i==(matriz.shape[0]+3) and j<matriz.shape[1]):
                        Txt3_1.insert(0,'%g'%(round(Cj_Zj[j-1],2)))
                if(j==0):
                    Txt3_1.insert(0,Labl[i])
                if(i==1 and j>0):
                    Txt3_1.insert(0,Var[j-1])
                if(i==0 and j>0 and j<(matriz.shape[1])):
                    Txt3_1.insert(0,'%g'%(Coef[j-1]))
        
        Btn2=tk.Button(newFrame, text="Continuar", width=60, command=lambda: calcular(Coef, Var,V_Base,base, matriz, Zj, Cj_Zj, tipo, paso))
        Btn2.grid(padx=1,pady=5,row=matriz.shape[0]+5,column=0, columnspan=matriz.shape[1])
        
        Fil, Col=Pivote(matriz, Cj_Zj, V_Base, tipo)
        
        Lbl3_1=tk.Label(newFrame, text='V. Ent: '+Var[Col])
        Lbl3_1.config(font=("Helvetica",15))
        Lbl3_1.grid(pady=5,row=matriz.shape[0]+6,column=0, columnspan=3)
        
        Lbl3_2=tk.Label(newFrame, text='V. Sal: '+V_Base[Fil])
        Lbl3_2.config(font=("Helvetica",15))
        Lbl3_2.grid(pady=5,row=matriz.shape[0]+7,column=0, columnspan=3)
        
        Lbl3_3=tk.Label(newFrame, text='Pivote: '+'%g'%(matriz[Fil][Col]))
        Lbl3_3.config(font=("Helvetica",15))
        Lbl3_3.grid(pady=5,row=matriz.shape[0]+8,column=0, columnspan=3)
        
        newFrame.pack()        
    else:
        newFrame.pack_forget()
        
        Lbl3=tk.Label(finalFrame, text="Metodo de la Gran M Terminado")
        Lbl3.config(font=("Helvetica",14))
        Lbl3.grid(pady=5,row=0,column=0, columnspan=matriz.shape[1]+2)
        
        Labl=np.concatenate((Labl, V_Base,['Zj','Cj-Zj']))
        for i in range(matriz.shape[0]+4):
            for j in range(matriz.shape[1]+1):
                Txt3_1=tk.Entry(finalFrame, width=6)
                Txt3_1.config(font=("Helvetica",12))
                Txt3_1.grid(row=i+1,column=j)
                
                if(i>1 and j>0 and j<(matriz.shape[1]+1)):
                    if(i<(matriz.shape[0]+2)):
                        Txt3_1.insert(0,'%g'%(round(matriz[i-2][j-1], 2)))
                    if(i==(matriz.shape[0]+2)):            
                        Txt3_1.insert(0,'%g'%(round(Zj[j-1],2)))
                    if(i==(matriz.shape[0]+3) and j<matriz.shape[1]):
                        Txt3_1.insert(0,'%g'%(round(Cj_Zj[j-1],2)))
                if(j==0):
                    Txt3_1.insert(0,Labl[i])
                if(i==1 and j>0):
                    Txt3_1.insert(0,Var[j-1])
                if(i==0 and j>0 and j<(matriz.shape[1])):
                    Txt3_1.insert(0,'%g'%(Coef[j-1]))
        for i in range(len(Var)-1):
            if('X' in Var[i]):
                Lbl3_1=tk.Label(finalFrame, text=Var[i]+' = ')
                Lbl3_1.config(font=("Helvetica",12))
                
                Lbl3_1.grid(pady=5,row=matriz.shape[0]+(6+i),column=0, columnspan=3)
                
                if(Var[i] in V_Base):  
                    b='%g'%(round(matriz[np.where(np.array(V_Base) == np.array(Var[i]))[0][0]][matriz.shape[1]-1],2))
                    Lbl3_2=tk.Label(finalFrame, text=b)
                else:
                    Lbl3_2=tk.Label(finalFrame, text=0)
                
                Lbl3_2.config(font=("Helvetica",12))
                Lbl3_2.grid(pady=5,row=matriz.shape[0]+(6+i),column=1, columnspan=3)
                
#        z='%g'%(round(Zj[len(Zj)-1],1))
        z=Zj[len(Zj)-1]
        z=f"{z:.0f}"
        Lbl3_4=tk.Label(finalFrame, text="Z = ")
        Lbl3_4.config(font=("Helvetica",12))
        Lbl3_4.grid(pady=5,row=matriz.shape[0]+6,column=3, columnspan=3)
        
        Lbl3_3=tk.Label(finalFrame, text=z)
        Lbl3_3.config(font=("Helvetica",12))
        Lbl3_3.grid(pady=3,row=matriz.shape[0]+6,column=4, columnspan=3)
    
        Btn2=tk.Button(finalFrame, text="Terminado", width=60)
        Btn2.grid(padx=1,pady=5,row=matriz.shape[0]+5,column=0, columnspan=matriz.shape[1])
        finalFrame.pack()
    
# =============================================================================
# Metodo que calcula cada paso de la solución para imprimirla en pantalla
# =============================================================================
def calcular(Coef, Var,V_Base,base, matriz, Zj, Cj_Zj, tipo, paso):

    """ Se verifica si hay variables artificiales en el vector de variables """
    if(FaseArt(Var)):
        """ Calcula una base auxiliar, utilizando la variable M """
        Aux=Zj_M(base, V_Base)
        """ Calcula la fila de variables, utilizando la variable M"""
        C=Zj_M(Coef, Var)
        """ Calcula Zj y Cj-Zj, de acuerdo a la variable M """
        Zj, Cj_Zj = CjZj(matriz, Aux, C)
        """ Calcula fila y columna pivote """
        Fil_Piv, Col_Piv=Pivote(matriz, Cj_Zj, V_Base, tipo)
        """ Realiza la eliminación gaussiana """
        matriz=Gauss(matriz, Fil_Piv, Col_Piv)
        """ Modifica las variables y coeficientes de la base """
        base[Fil_Piv]=Coef[Col_Piv]
        elim=V_Base[Fil_Piv]            
        V_Base[Fil_Piv]=Var[Col_Piv]
        
        """ Elimina la variable artificial que salió anteriormente de la base """
        for i in range(matriz.shape[1]-1):
            if(Var[i]==elim):
                matriz=np.delete(matriz, i,axis=1)
                Var=np.delete(Var, i)
                Coef=np.delete(Coef, i)
        """ Calcula fila Zj y Cj-Zj """
        Zj, Cj_Zj = CjZj(matriz, base, Coef)
        """ Imprime el resultado """
        imprimir(Coef, Var, V_Base,base, matriz, Zj, Cj_Zj, tipo, paso+1, FaseArt(Var))
    
    else:
        """  Si no se encuentran variables artificiales despues de ser eliminadas las columnas de la matriz """
        """  Calcula fila y columna pivote """
        Fil_Piv, Col_Piv=Pivote(matriz, Cj_Zj, V_Base, tipo)
        """ Realiza eliminación gaussiana """
        matriz=Gauss(matriz, Fil_Piv, Col_Piv)       
        """ Modifica variables y coeficientes de la base """
        base[Fil_Piv]=Coef[Col_Piv]
        V_Base[Fil_Piv]=Var[Col_Piv]
        """ Calcula filas de Zj y Cj-Zj """
        Zj, Cj_Zj = CjZj(matriz, base, Coef)        
        """ Imprime el resultado """
        imprimir(Coef, Var, V_Base, base, matriz, Zj, Cj_Zj, tipo, paso+1, FaseArt(Var))
        
        
# =============================================================================
# Método que determina la ejecución de acuerdo a las variables artificiales
# =============================================================================
def FaseArt(Var):
    continuar=False
    for i in range(len(Var)):
        if('A' in Var[i]):
            continuar=True
    return continuar

# =============================================================================
# Determina Fila y Columna Pivote
# =============================================================================
    
def Pivote(matriz, Cj_Zj, V_Base, tipo):
    
    if (tipo == 'Minimizar'):
        Col_Piv=np.where(Cj_Zj==min(Cj_Zj))[0][0]
    else:
        Col_Piv=np.where(Cj_Zj==max(Cj_Zj))[0][0]
    b=matriz[:,matriz.shape[1]-1]
    
    Col=[]
    for i in range(matriz.shape[0]):
        Col.append(matriz[i][Col_Piv])
    
    Col=np.array(Col)
    delt=np.where(Col<=0)[0]
    
    Col[delt]=-1
    
    div=b/Col
    
    div[delt]=-1
        
    Fil_Piv=np.where(div==min(div[div>=0]))[0]
    
    if(FaseArt(V_Base)):
        for i in range(len(Fil_Piv)):
            if('A' in V_Base[Fil_Piv[i]]):
                Fil_Piv=Fil_Piv[i]
                break
    else:
        Fil_Piv=Fil_Piv[len(Fil_Piv)-1]
        
    return Fil_Piv, Col_Piv

# =============================================================================
# Modifica la base de acuerdo al coeficiente M
# =============================================================================
def Zj_M(base, V_Base):
    M=1000000
    Aux=[]
    
    for i in range(len(base)):
        if ('A' in V_Base[i]):
            Aux.append(base[i]*M)
        else:
            Aux.append(base[i]) 
    return Aux

# =============================================================================
# Metodo de Eliminación por Gauss
# =============================================================================
        
def Gauss(matriz, Fil_Piv, Col_Piv):
    matriz[Fil_Piv]/=matriz[Fil_Piv][Col_Piv]
    for i in range(matriz.shape[0]):
        if(i!=Fil_Piv):
            m=matriz[i][Col_Piv]
            matriz[i]=(matriz[Fil_Piv]*(m*-1))+matriz[i]
    return matriz

# =============================================================================
# Método que determina la fila de Cj-Zj
# =============================================================================

def CjZj(matriz, base, Coef):
    Zj=np.zeros(matriz.shape[1],dtype=float)
        
    for i in range(matriz.shape[0]):
        n=base[i]*matriz[i]
        Zj=n+Zj
        
    Cj_Zj=np.array(Coef+(Zj[0:len(Zj)-1]*-1))
    
    return Zj, Cj_Zj

# =============================================================================
# Metodo que verifica si el proceso de iteraciones terminó
# =============================================================================
    
def terminar(tipo, Cj_Zj):
    terminado=True
    for i in range(len(Cj_Zj)):
        if(tipo=='Maximizar'):
            if(Cj_Zj[i]>0):
                terminado=False
        if(tipo=='Minimizar'):
            if(Cj_Zj[i]<0):
                terminado=False
    return terminado

main()

raiz.mainloop()

