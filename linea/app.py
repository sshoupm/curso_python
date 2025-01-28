# cálculo de coordenadas de líneas
import argparse
import funcioness

def main(m:float, b:float):
    '''
    Función principal que calcula las 
    coordenadas de una línea recta. 
    Recibimos m y b.
    Regresa: nada 
    '''
    X=[x/10.0 for x in range(10,110,5)]
    Y=[funcioness.calcular_y(x,m,b) for x in X]
    coordenadas_flotantes=list(zip(X,Y))
    print("Florantes:")
    print(coordenadas_flotantes)
    funcioness.grafica_linea(X,Y,m,b)

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('-m', type=float, help='Pendiente de la línea', default=2.0)
    parser.add_argument('-b', type=float, help='Ordenada al origen', default=3.0)
    args=parser.parse_args()
    main(args.m, args.b)
    #main(m=2.0,b=3.0)