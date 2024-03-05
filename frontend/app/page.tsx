import { getFrameMetadata } from '@coinbase/onchainkit/frame';
import type { Metadata } from 'next';
import { NEXT_PUBLIC_URL } from './config';

const frameMetadata = getFrameMetadata({
  buttons: [
    {
      label: 'Kwentize!',
    },
    {
      action: 'link',
      label: 'Start trading!',
      target: 'https://kwenta.eth.limo/?ref=kwendroid',
    }
  ],
  image: {
    src: `${NEXT_PUBLIC_URL}/kwentize.png`,
    aspectRatio: '1:1',
  },
  postUrl: `${NEXT_PUBLIC_URL}/api/relay`,
});

export const metadata: Metadata = {
  title: 'https://github.com/AsparAugustus',
  description: 'LFG',
  openGraph: {
    title: 'https://github.com/AsparAugustus',
    description: 'LFG',
    images: [`${NEXT_PUBLIC_URL}/kwentize.png`],
  },
  other: {
    ...frameMetadata,
  },
};

export default function Page() {
  return (
    <>
      <h1>https://github.com/AsparAugustus</h1>
    </>
  );
}
