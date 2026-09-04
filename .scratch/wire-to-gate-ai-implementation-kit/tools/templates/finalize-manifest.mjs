//! Content-manifest finalizer, written verbatim into <candidate>/tools/finalize-manifest.mjs by
//! generate-protocol-candidate.mjs. Lines starting with `//!` are stripped on write;
//! double-underscore placeholders are substituted from the generator identity constants.
//! Edit this file, never the generated copy.
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
const root=path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/,"$1")),"..");
const sha=b=>crypto.createHash("sha256").update(b).digest("hex");
const canon=v=>v===null||typeof v!=="object"?JSON.stringify(v):Array.isArray(v)?"["+v.map(canon).join(",")+"]":"{"+Object.keys(v).sort().map(k=>JSON.stringify(k)+":"+canon(v[k])).join(",")+"}";
const excluded=p=>p==="manifest/release.json"||p.startsWith("attestations/")||p.startsWith(".git/")||p.startsWith("node_modules/")||p.startsWith("evidence/")||p.startsWith(".github/");
const walk=d=>fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>{const p=path.join(d,e.name);return e.isDirectory()?walk(p):[p]});
const files=walk(root).map(p=>path.relative(root,p).replaceAll("\\","/")).filter(p=>!excluded(p)).sort().map(p=>{const b=fs.readFileSync(path.join(root,p));return{path:p,role:p.split("/")[0],bytes:b.length,sha256:sha(b)}});
const combine=prefix=>sha(Buffer.from(files.filter(f=>f.path.startsWith(prefix)).map(f=>f.path+":"+f.sha256).join("\n")+"\n"));
const seed=JSON.parse(fs.readFileSync(path.join(root,"manifest/release.json"),"utf8"));
const manifest={status:"CONTENT_SNAPSHOT",releaseVersion:"__CANDIDATE_VERSION__",protocolVersion:__PROTOCOL_VERSION__,profileId:"__PROFILE_ID__",repository:"8005-agv-protocol",generatedAt:"__CANDIDATE_TIMESTAMP__",hashAlgorithm:"SHA-256",jsonCanonicalization:"RFC8785-compatible sorted-key JCS for semantic collections; raw bytes for file entries",fileTableSha256:sha(Buffer.from(canon(files))),schemaBundleSha256:combine("schemas/"),examplesSha256:combine("examples/"),vectorsSha256:combine("vectors/"),errorRegistrySha256:combine("errors/"),messages:seed.messages,denylistedMessageTypes:seed.denylistedMessageTypes,files};
fs.mkdirSync(path.join(root,"manifest"),{recursive:true});fs.writeFileSync(path.join(root,"manifest/release.json"),JSON.stringify(manifest,null,2)+"\n");console.log(JSON.stringify({manifestSha256:sha(fs.readFileSync(path.join(root,"manifest/release.json"))),files:files.length,messageTypeCount:Object.keys(manifest.messages).length,status:manifest.status},null,2));
