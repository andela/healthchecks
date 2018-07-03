num_checks = 10
num_channels = 10
result = ""

if num_checks <= 1 and num_channels <= 1:
    result =  "%d checks, %d channels" % (num_checks, num_channels)
else:
    result = "<strong>%d checks </strong>, <strong>%d channels</strong>" %(num_checks, num_channels)

print result
