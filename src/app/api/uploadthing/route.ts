// UPLOAD FEATURE DISABLED - Comment out UploadThing route handlers
// import { createRouteHandler } from 'uploadthing/next';
// import { ourFileRouter } from '@/lib/uploadthing';
// export const { GET, POST } = createRouteHandler({ router: ourFileRouter });

// Return 503 Service Unavailable for upload endpoints while disabled
export async function GET() {
  return new Response('Upload service is currently disabled', { 
    status: 503,
    statusText: 'Service Unavailable' 
  });
}

export async function POST() {
  return new Response('Upload service is currently disabled', { 
    status: 503,
    statusText: 'Service Unavailable' 
  });
}
