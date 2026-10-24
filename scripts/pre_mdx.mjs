import fs from "fs";
const { compile } = await import("@mdx-js/mdx");
const files = process.argv.slice(2);
let ok = 0, bad = [];
for (const f of files) {
  try { await compile(fs.readFileSync(f, "utf8"), { format: "mdx" }); ok++; }
  catch (e) { bad.push([f, e.message.split("\n")[0]]); }
}
console.log("MDX " + ok + "/" + files.length);
for (const [f, m] of bad) console.log("FAIL", f, m);
