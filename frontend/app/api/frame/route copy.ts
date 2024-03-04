import { FrameRequest, getFrameMessage, getFrameHtmlResponse } from '@coinbase/onchainkit/frame';
import { NextRequest, NextResponse } from 'next/server';
import { NEXT_PUBLIC_URL } from '../../config';
import { NeynarAPIClient, isApiErrorResponse } from "@neynar/nodejs-sdk";
import axios from "axios";

const apiKey = process.env.NEYNAR_APIKEY;
if (apiKey) {
  const client = new NeynarAPIClient(apiKey);
  // Use client
} else {
  // Handle the missing API key case, e.g., throw an error or log a warning
  console.error("No API key found")
}
async function getResponse(req: NextRequest): Promise<NextResponse> {

  const options = {
    method: 'POST',
    headers: {
      accept: 'application/json',
      api_key: 'NEYNAR_API_DOCS',
      'content-type': 'application/json'
    },
    body: JSON.stringify({
      cast_reaction_context: true,
      follow_context: false,
      message_bytes_in_hex: '0a49080d1085940118f6a6a32e20018201390a1a86db69b3ffdf6ab8acb6872b69ccbe7eb6a67af7ab71e95aa69f10021a1908ef011214237025b322fd03a9ddc7ec6c078fb9c56d1a72111214e3d88aeb2d0af356024e0c693f31c11b42c76b721801224043cb2f3fcbfb5dafce110e934b9369267cf3d1aef06f51ce653dc01700fc7b778522eb7873fd60dda4611376200076caf26d40a736d3919ce14e78a684e4d30b280132203a66717c82d728beb3511b05975c6603275c7f6a0600370bf637b9ecd2bd231e'
    })
  };
  
  const response = fetch('https://api.neynar.com/v2/farcaster/frame/validate', options)
    .then(response => response.json())
    .then(response => console.log(response))
    .catch(err => console.error(err));



  let accountAddress: string | undefined = '';
  let text: string | undefined = '';

  const body: FrameRequest = await req.json();
  const { isValid, message } = await getFrameMessage(body, { neynarApiKey: 'NEYNAR_ONCHAIN_KIT' });

  if (isValid) {
    accountAddress = message.interactor.verified_accounts[0];
  }

  if (message?.input) {
    text = message.input;
  }

  // if (message?.button === 3) {
  //   return NextResponse.redirect(
  //     'https://www.google.com/search?q=cute+dog+pictures&tbm=isch&source=lnms',
  //     { status: 302 },
  //   );
  // }

 

  if (message?.button === 3) {
    return NextResponse.redirect(
      `https://`,
      { status: 302 },
    );
  }

  return new NextResponse(
    getFrameHtmlResponse({
      buttons: [
        {
          label: `Story: ${text} 🌲🌲`,
        },
      ],
      image: {
        src: `${NEXT_PUBLIC_URL}/park-1.png`,
      },
      postUrl: `${NEXT_PUBLIC_URL}/api/frame`,
    }),
  );
}

export async function POST(req: NextRequest): Promise<Response> {
  return getResponse(req);
}

export const dynamic = 'force-dynamic';
