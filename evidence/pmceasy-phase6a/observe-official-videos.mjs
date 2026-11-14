// Bounded public demonstration observation only; no video download, HAR or session export.
import { chromium } from '../../frontend/node_modules/playwright-core/index.mjs'
import { mkdir, writeFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
const root=fileURLToPath(new URL('./',import.meta.url))
await mkdir(root+'videos',{recursive:true})
const browser=await chromium.launch({headless:true})
const records=[]
const batches={base:[['iEMJeuOXkq4',[150,240,330]],['1GHKNwNkL6Q',[150,240,330]]],
  followup:[['iEMJeuOXkq4',[180,200,220,280]],['1GHKNwNkL6Q',[90,120]]],
  intake:[['1GHKNwNkL6Q',[100,105,110]],['iEMJeuOXkq4',[210,300]]]}
const batch=process.argv[2]||'intake'
if(!batches[batch]){await browser.close();throw new Error('UNKNOWN_RESEARCH_BATCH')}
try {
  const context=await browser.newContext({viewport:{width:1440,height:1000},serviceWorkers:'block'})
  await context.route('**/*',route=>{
    const host=new URL(route.request().url()).hostname
    return ['www.youtube.com','youtube.com','www.youtube-nocookie.com','i.ytimg.com','s.ytimg.com','fonts.gstatic.com','www.gstatic.com','jnn-pa.googleapis.com','youtubei.googleapis.com'].includes(host) || host.endsWith('.googlevideo.com') ? route.continue():route.abort()
  })
  for(const [id,times] of batches[batch]){
   for(const start of times){
    const page=await context.newPage()
    const record={id,url:`https://www.youtube.com/watch?v=${id}&t=${start}s`,frames:[]}
    try {
      const response=await page.goto(record.url,{waitUntil:'domcontentloaded',timeout:35000})
      await page.waitForTimeout(3500)
      record.http_status=response?.status()
      record.title=await page.title()
      // Public playback only; never sign in or accept a payment/access challenge.
      const video=page.locator('video').first()
      if(!await video.count()) throw new Error('NO_PUBLIC_VIDEO_ELEMENT')
      await video.evaluate(v=>{v.muted=true; return v.play().catch(()=>undefined)})
      await page.waitForTimeout(3500)
      record.playback=await video.evaluate(v=>({duration:Number.isFinite(v.duration)?v.duration:null,ready_state:v.readyState,video_width:v.videoWidth,video_height:v.videoHeight,error_code:v.error?.code??null}))
      if(!record.playback.video_width || !record.playback.duration) throw new Error('NO_DECODED_PUBLIC_VIDEO_FRAMES')
      const expectedDuration=id==='iEMJeuOXkq4'?399.581:371.601
      if(Math.abs(record.playback.duration-expectedDuration)>2) throw new Error('UNOBSERVED_MEDIA_IDENTITY_DURATION_MISMATCH')
      for(const time of [start]){
        if(time>=record.playback.duration) continue
        const decoded=await video.evaluate((v,t)=>new Promise(resolve=>{
          let done=false
          const timer=setTimeout(()=>{if(!done){done=true;v.pause();resolve({ok:false,seeking:v.seeking,ready_state:v.readyState,clock:v.currentTime})}},20000)
          const sample=(_now,meta)=>{
            if(done)return
            if(Math.abs(meta.mediaTime-t)<2 && !v.seeking){done=true;clearTimeout(timer);v.pause();resolve({ok:true,media_time:meta.mediaTime,clock:v.currentTime})}
            else v.requestVideoFrameCallback(sample)
          }
          v.currentTime=t
          v.requestVideoFrameCallback(sample)
          v.play().catch(()=>undefined)
        }),time)
        if(!decoded.ok){record.frames.push({requested_seconds:time,status:'UNOBSERVED_SEEK_NO_DECODED_FRAME',diagnostic:decoded});break}
        const actual=decoded.clock
        const path=`videos/${id}-${time}s-cropped.png`
        const box=await video.boundingBox()
        const clip={x:box.x+box.width*.02,y:box.y+box.height*.18,width:box.width*.96,height:box.height*.72}
        await page.screenshot({path:root+path,clip})
        record.frames.push({requested_seconds:time,actual_seconds:actual,decoded_media_seconds:decoded.media_time,path,crop_fraction:{left:.02,top:.18,width:.96,height:.72},privacy_note:'Browser URL/profile/account header and bottom strip excluded. Manual content review still required.'})
      }
    }catch(error){record.limitation=String(error.message).split('\n')[0].slice(0,120)}
    await page.close();records.push(record)
   }
  }
  await context.close()
}finally{await browser.close()}
const manifestName=batch==='base'?'observation-manifest.json':`observation-manifest-${batch}.json`
await writeFile(root+'videos/'+manifestName,JSON.stringify({kind:'PUBLIC_OFFICIAL_DEMONSTRATION_NOT_LIVE_PRODUCT',date:'2026-11-14',records,limitations:['Fresh owned temporary browser profile. Only the two selected official video pages and required media/assets allowed. No login, payment, saved cookies, headers, caption URLs, signed media URLs, request bodies, unrelated browsing or video-file download. Seeking a published demo does not execute the demonstrated PMCEASY product.']},null,2)+'\n')
console.log(JSON.stringify(records))
