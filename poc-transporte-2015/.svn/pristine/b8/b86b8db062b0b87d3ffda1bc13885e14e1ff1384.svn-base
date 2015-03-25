import sched, time
def dostuff(test):
  print "stuff is being done!" + test
  s.enter(3, 1, lambda: dostuff(" testando o argumento denovo"), ())

s = sched.scheduler(time.time, time.sleep)
s.enter(3, 1, lambda: dostuff(" testando o argumento"), ())
s.run()