import React from 'react';
import * as schema from 'schemawax';
import './App.css';

type Props = {
    apiUrl: string
}

type HelloMessage = {
    message: string
}

const helloMessageDecoder: schema.Decoder<HelloMessage> =
    schema.object({
        required: {message: schema.string},
    });

export const App: React.FC<Props> = ({apiUrl}: Props) => {
    const [message, setMessage] = React.useState('');

    React.useEffect(() => {
        const fetchMessage = async () => {
            try {
                const response = await fetch(`${apiUrl}/api/hello`);
                const json: unknown = await response.json();
                const decodeResult = helloMessageDecoder.validate(json);

                switch (decodeResult.type) {
                    case 'ok':
                        setMessage(decodeResult.data.message);
                        break;
                    case 'error':
                        setMessage('Error decoding the response');
                        break;
                }
            } catch {
                setMessage('Connection error or invalid json');
            }
        };

        fetchMessage().then();
    }, [apiUrl]);

    return (
        <section>{message}</section>
    );
};
