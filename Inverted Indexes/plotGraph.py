import matplotlib.pyplot as plt

if __name__=='__main__':
    f = open("time.txt")
    
    line = f.readline()
    lines = line.split(" ")
    linear_length = []
    linear_time = []
    for i in range(0, len(lines)-1,2):
        linear_length.append(int(lines[i]))
        linear_time.append(float(lines[i+1]))
    
    line = f.readline()
    lines = line.split(" ")
    binary_length = []
    binary_time = []
    for i in range(0, len(lines)-1,2):
        binary_length.append(int(lines[i]))
        binary_time.append(int(lines[i+1]))

    line = f.readline()
    lines = line.split(" ")
    galloping_length = []
    galloping_time = []
    for i in range(0, len(lines)-1,2):
        galloping_length.append(int(lines[i]))
        galloping_time.append(int(lines[i+1]))

    fig, (ax1,ax2,ax3) = plt.subplots(1,3)
    plt.title("Response Time VS Length of Queries")
    ax1.scatter(linear_length, linear_time, color="red")
    ax2.scatter(binary_length, binary_time, color="orange")
    ax3.scatter(galloping_length, galloping_time, color="green")

    plt.show()