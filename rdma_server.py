# Name: rdma_server.py
# Purpose: Demonstrate RDMA server using iWARP


import socket
from pyverbs import Context, PD, CQ, MR, RCQP

def main():
    # Create RDMA context
    ctx = Context()
    pd = PD(ctx)
    cq = CQ(ctx)
    
    # Create a Queue Pair (QP)
    qp = RCQP(pd, cq, cq, max_send=1, max_recv=1)
    qp.create()

    # Bind the QP to a local address (simulate with localhost)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 12345))
    sock.listen(1)

    print("Waiting for a connection...")
    conn, addr = sock.accept()
    print("Connected by", addr)

    # Perform RDMA operations
    data = b"Hello, RDMA!"
    mr = MR(pd, data)
    qp.send(mr)

    print("Sent data:", data)

    # Clean up
    mr.dereg()
    qp.destroy()
    cq.destroy()
    pd.release()
    ctx.release()
    sock.close()

if __name__ == "__main__":
    main()
