import { FrameRequest, getFrameMessage, getFrameHtmlResponse } from '@coinbase/onchainkit/frame';
import { NextRequest, NextResponse } from 'next/server';
import { NEXT_PUBLIC_URL, NEXT_API_URL } from '../../config';
import { NeynarAPIClient, isApiErrorResponse } from "@neynar/nodejs-sdk";
import axios from "axios";

//1st frame goes to frame that generates
//2nd frame
//generate pfp, 

enum ResponseType {
  SUCCESS,
  RECAST,
  ALREADY_MINTED,
  NO_ADDRESS,
  OUT_OF_GAS,
  ERROR,
}



const NEYNAR_API_KEY = process.env.NEYNAR_API_KEY;
export const dynamic = 'force-dynamic';

let user = {
  custody_address: null,
  username: null,
  display_name: null,
  pfp_url: null,
  
}


export async function POST(req: NextRequest): Promise<Response> {

  const body: { trustedData?: { messageBytes?: string } } = await req.json();

  // Check if frame request is valid
  const status = await validateFrameRequest(body.trustedData?.messageBytes);

  if (!status?.valid) {
    console.error(status);
    throw new Error('Invalid frame request');
  }

  //need to fetch user's
  //1. custody address? verified addresses?
  //2. username
  //3. display_name
  //4. pfp url

  user.custody_address = status.action.interactor.custody_address
  user.username = status.action.interactor.username
  user.display_name = status.action.interactor.display_name
  user.pfp_url = status.action.interactor.pfp_url

  //follower count? following count?



  // return getResponse(ResponseType.SUCCESS);

  const encodedCustodyAddress = user.custody_address !== null ? encodeURIComponent(user.custody_address) : "";
  const encodedUsername = user.username !== null ? encodeURIComponent(user.username) : "";
  const encodedPfpUrl = user.pfp_url !== null ? encodeURIComponent(user.pfp_url) : "";

  return new NextResponse(
    getFrameHtmlResponse({
      buttons: [
        {
          label: `Start conversion!`,
        }
      ],
      image: {
        src: `${NEXT_PUBLIC_URL}/kwentize_1.png`,
      },
      postUrl: `${NEXT_PUBLIC_URL}/api/relay`,
    }),
  );

}


function getResponse(type: ResponseType) {
  const IMAGE = {
    [ResponseType.SUCCESS]: 'status/success.png',
    [ResponseType.RECAST]: 'status/recast.png',
    [ResponseType.ALREADY_MINTED]: 'status/already-minted.png',
    [ResponseType.NO_ADDRESS]: 'status/no-address.png',
    [ResponseType.OUT_OF_GAS]: 'status/out-of-gas.png',
    [ResponseType.ERROR]: 'status/error.png',
  }[type];
  const shouldRetry =
    type === ResponseType.ERROR || type === ResponseType.RECAST;

    console.log(IMAGE)

  

    return new NextResponse(
      getFrameHtmlResponse({
        buttons: [
          {
            label: `${user.custody_address}`,
          },
          {
            label: `${user.display_name}`,
          },
          {
            label: `${user.username}`,
          }
        ],
        image: {
          src: `${user.pfp_url}`,
        },
        postUrl: `${NEXT_API_URL}/api/generate`,
      }),
    );



  // return new NextResponse(`<!DOCTYPE html><html><head>
  //   <meta property="fc:frame" content="vNext" />
  //   <meta property="fc:frame:image" content="${NEXT_PUBLIC_URL}/${IMAGE}" />
  //   <meta property="fc:frame:post_url" content="${NEXT_PUBLIC_URL}/api/frame" />
  //   ${ 
  //     shouldRetry
  //       ? `<meta property="fc:frame:button:1" content="Try again" />`
  //       : ''
  //   }
  // </head></html>`);
}



async function validateFrameRequest(data: string | undefined) {
  if (!NEYNAR_API_KEY) throw new Error('NEYNAR_API_KEY is not set');
  if (!data) throw new Error('No data provided');

  const options = {
    method: 'POST',
    headers: {
      accept: 'application/json',
      api_key: NEYNAR_API_KEY,
      'content-type': 'application/json',
    },
    body: JSON.stringify({ message_bytes_in_hex: data }),
  };

  return await fetch(
    'https://api.neynar.com/v2/farcaster/frame/validate',
    options,
  )
    .then((response) => response.json())
    .catch((err) => console.error(err));
}