
###
predict <- Predict(fit,njn,fun=function(x)exp(x))
pdf(file="D:\\Users\\XMK1\\Desktop\\analysis result\\elasticsearch\\predict_njn.pdf"
    , width = 11, height = 8.5)
plot(predict, ylab='Odds')
dev.off()

predict <- Predict(fit,integrator,fun=function(x)exp(x))
pdf(file="D:\\Users\\XMK1\\Desktop\\analysis result\\elasticsearch\\predict_integrator.pdf"
    , width = 11, height = 8.5)
plot(predict, ylab='Odds')
dev.off()


# #