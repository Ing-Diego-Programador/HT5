
#   Diego Vásquez - 211628
#   Universidad del Valle de Guatemala
#   Hoja de trabajo 5 - Algoritmos y estructura de datos.

import random
import simpy


#Función  con los procesos para la simulación.
def simulacion(env, ci_Instrucciones, intrucciones, nombre, c_Ram, c_Operaciones, r_Inicial, nucleos, wait): 

    start = env.now
    
    yield env.timeout(wait)
    print("%s En etapa New | RAM requerida: %d | RAM disponible: %d" % (nombre, c_Ram, r_Inicial.level))
    yield r_Inicial.get(c_Ram)
    print("%s En etapa Ready | Instrucciones pendientes %d" % (nombre, ci_Instrucciones))

    #Ciclos de cada operacion, proceso de cola en waiting, timepo de espera y retornar a running.
    cont = 0
    while cont == 0:
        if ci_Instrucciones > 0:
            with nucleos.request() as req:
                yield req
                ci_Instrucciones -= intrucciones
                yield env.timeout(c_Operaciones) 
                print("%s En etapa ready | Instrucciones pendientes %d" % (nombre, ci_Instrucciones))

            if ci_Instrucciones > 0:
                evento_random = random.randint(1, 2)
                if evento_random == 1:
                    print("%s Se ha ingresado a la etapa waiting" % (nombre))
                    yield env.timeout(random.randint(1, 5)) 
                else:
                    pass 
        else:
            cont = 1

    yield r_Inicial.put(c_Ram)
    global timepoT
    timepoT += env.now - start
    print("%s Terminado | Cantidad de RAM devuelta: %d | Cantidad de memoria disponible %d" % (nombre, c_Ram, r_Inicial.level))


env = simpy.Environment()
# Propiedades de la simulacion.
intervalos = 1 
timepoT = 0 
i_Ciclo = 3
op_Ciclo = 1
c_Procesos = 200  
s_Ram = simpy.Container(env, init=100, capacity=100) 
r_Inicial = s_Ram
nucleos = simpy.Resource(env, capacity=2)

for i in range(c_Procesos):
    wait = random.expovariate(1.0/10)
    ci_Instrucciones = random.randint(1, 10)
    c_Ram = random.randint(1, 10)
    env.process(simulacion(env=env, wait=wait, nombre="Proceso %d" % i, c_Ram=c_Ram, ci_Instrucciones=ci_Instrucciones, intrucciones=i_Ciclo, c_Operaciones=op_Ciclo, r_Inicial=r_Inicial, nucleos=nucleos))

env.run()
#Toma de tiempo para el analisís y las gráficas.
tiempo_promedio = timepoT/c_Procesos
print("tiempo promedio: %d milisegundos" % (tiempo_promedio))