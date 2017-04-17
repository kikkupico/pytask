import asyncio
import functools


class ExecutorProtocol(asyncio.SubprocessProtocol):

    FD_NAMES = ['stdin', 'stdout', 'stderr']

    def __init__(self, done_future):
        self.done = done_future
        self.buffer = bytearray()
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport

    def pipe_data_received(self, fd, data):
        print('read {} bytes from {}'.format(len(data),
                                             self.FD_NAMES[fd]))
        if fd == 1:
            self.buffer.extend(data)

    def process_exited(self):
        return_code = self.transport.get_returncode()
        if not return_code:
            cmd_output = bytes(self.buffer).decode()
            results = self.handle_process_output(cmd_output)
        else:
            results = []
        self.done.set_result((return_code, results))

    def handle_process_output(self, output):
        print(output)
        return output


async def run_command_async(loop, cmd):
    print('Tryin to run ' + cmd)
    cmd_done = asyncio.Future(loop=loop)
    factory = functools.partial(ExecutorProtocol, cmd_done)
    proc = loop.subprocess_shell(
        factory,
        cmd,
        stdin=None,
        stderr=asyncio.subprocess.STDOUT,
        stdout=None
    )
    try:
        transport, protocol = await proc
        await cmd_done
    finally:
        transport.close()

    return cmd_done.result()
