class myclass():
    myUrls = ['asdasd',]

    def addVals(self):
        for i in range(1,7):
            self.myUrls.append(i)

    def start(self):
        for i in self.myUrls:
            print(i)
            self.addVals()

asda = myclass()

asda.start()