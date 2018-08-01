from gateway import AfricasTalkingGateway

def sendsms(to, message):
    gateway = AfricasTalkingGateway("sandbox", "657d265600a307dac2e623fca122f9a71703e28eaa10175cd6815b136562cb3f")
    results = gateway.sendMessage(to, message)
    return results


sendsms("+254790463533", "Hello Abraham")