# Name: rdma_client.py
# Purpose: Demonstrate RDMA client using iWARP
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

    # Connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 12345))

    # Receive data
    mr = MR(pd, b'\x00' * 32)  # Allocate memory for receiving data
    qp.recv(mr)

    print("Received data:", mr.buf[:len(mr.buf)].tobytes().decode())

    # Clean up
    mr.dereg()
    qp.destroy()
    cq.destroy()
    pd.release()
    ctx.release()
    sock.close()

if __name__ == "__main__":
    main()
