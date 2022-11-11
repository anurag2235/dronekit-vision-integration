import multiprocessing
result = []
  
def square_list(mylist):
    """
    function to square a given list
    """
    global result
    # append squares of mylist to global list result
    for num in mylist:
        result.append(num * num)
    # print global list result
    print("Result(in process p1): {}".format(result))
if __name__ == "__main__":
    # input list
    mylist = [1,2,3,4]
  
    # creating new process
    p1 = multiprocessing.Process(target=square_list, args=(mylist,))
    # starting process
    p1.start()
    # wait until process is finished
    p1.join()
  
    # print global result list
    print("Result(in main program): {}".format(result))