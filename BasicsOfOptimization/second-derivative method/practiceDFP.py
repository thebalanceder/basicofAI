import numpy as np

def f(x):
    return (x[0]-1)**2+(x[1]-2)**2

def grad_f(x):
    return np.array([2*(x[0]-1),2*(x[1]-2)])

def dfp(f,grad_f,x0,tol=1e-6,max_iter=1000):

    x_k=np.array(x0)
    n=len(x_k)
    B_k=np.eye(n)
    k=0

    while k<max_iter:
        
        grad_k=grad_f(x_k)

        if np.linalg.norm(grad_k)<tol:
            print(f"max iteration at{k}")
            break
        
        p_k=-B_k@grad_k
        alpha=line_search(f,x_k,p_k)

        x_new=x_k+alpha*p_k
        y_k=grad_f(x_new)-grad_k
        s_k=x_new-x_k
        item1=np.outer(s_k,s_k)/np.dot(s_k,y_k)
        item2=B_k@np.outer(y_k,y_k)@B_k/np.dot(y_k,B_k@y_k)
        B_k=B_k+item1-item2

        x_k=x_new
        k+=1
        
    return x_k


def line_search(f,x_k,p_k,alpha=1,rhio=.8,c=1e-6):
    if f(x_k+alpha*p_k)>f(x_k)+c*alpha*np.dot(grad_f(x_k),p_k):
        alpha*=rhio
    return alpha

x0=np.array([0,0])
optimzal_x=dfp(f,grad_f,x0)
print(f"optmal point:{optimzal_x}")
