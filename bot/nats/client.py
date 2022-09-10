import asyncio
import nats


async def main():
    nc = await nats.connect('nats://localhost:4222')

    # Publish as message with an inbox.
    inbox = nc.new_inbox()
    sub = await nc.subscribe('KonstantinArkov')

    # Simple publishing
    # await nc.publish('hello', b'Hello World!')

    # Publish with a reply
    # await nc.publish('hello', b'Hello World!', reply=inbox)

    # Publish with a reply
    # await nc.publish('hello', b'With Headers', headers={'Foo': 'Bar'})

    while True:
        try:
            msg = await sub.next_msg()
            print('----------------------')
            print('Subject:', msg.subject)
            print('Reply  :', msg.reply)
            print('Data   :', msg.data)
            print('Headers:', msg.header)
        except:
            pass


if __name__ == '__main__':
    asyncio.run(main())
