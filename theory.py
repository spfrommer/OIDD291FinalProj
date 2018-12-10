import random

pic = 1361.104
pid = 187.5
piu = 1816.5
pil = 518.368
pin = 520.833
pidn = 1426.557

def trigger_payoff(phat, nhat):
    return 2*pic + pic*(1-nhat) + pil*(nhat) + 2*(pic*(1-nhat)+pid*nhat)
    
def sneaky_payoff(phat, nhat):
    return piu + pic * phat + pil * (1-phat) + pic * phat * (1-nhat) + pin * (1-phat) + pil * phat * nhat +2*(pic*phat*(1-nhat)+pin*(1-phat+phat*nhat))
    
def defect_payoff(phat, nhat):
    return 2*pic+nhat*pin+(1-nhat)*pidn + 2 * (1-nhat) * pid + 2 * nhat * pic

    #return 2*pic+nhat*pin+(1-nhat)*pidn + 2 * (1-nhat) * pid + 2 * nhat * pin

#def trigger_payoff(phat, nhat):
    #return 2*pic + pic*(1-nhat) + pil*(nhat)
    
#def sneaky_payoff(phat, nhat):
    #return piu + pic * phat + pil * (1-phat) + pic * phat * (1-nhat) + pid * (1-phat) + pil * phat * nhat
   
#def defect_payoff(phat, nhat):
    #return 2*pic+nhat*pin+(1-nhat)*(pidn + 105*pid) / 106

#def defect_payoff(phat, nhat):
    #return 2*pic+nhat*pin+(1-nhat)*(pidn)
    #return 2*pic+nhat*pid+(1-nhat)*piu
