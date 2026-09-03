// Builds the generic cover letter. Shares the resume's letterhead and palette.
// Run: node build_letter.js
const {
  Document, Packer, Paragraph, TextRun, BorderStyle, convertInchesToTwip,
} = require('docx');
const fs = require('fs');

const INK   = '0F1319';
const GREEN = '1F8A65';
const GRAY  = '5A6472';
const FONT  = 'Calibri';
const BODY  = 21;   // 10.5pt — a letter reads larger than a resume

const t = (text, o = {}) => new TextRun({ text, font: FONT, color: INK, size: BODY, ...o });
const para = (text, o = {}) => new Paragraph({
  spacing: { before: 120, after: 120, line: 290 },
  children: Array.isArray(text) ? text : [t(text)],
  ...o,
});

const children = [];

// ── Letterhead, matching the resume ─────────────────────────────────────────
children.push(new Paragraph({
  spacing: { after: 0 },
  children: [
    t('Jess Ferretti', { bold: true, size: 40 }),
    t('   (she/her)', { size: 19, color: GRAY }),
  ],
}));
children.push(new Paragraph({
  spacing: { before: 40, after: 60 },
  children: [t('Enterprise Sales Leader  ·  Go-to-Market & Revenue Growth', { bold: true, color: GREEN, size: 22 })],
}));
children.push(new Paragraph({
  spacing: { after: 0 },
  children: [t('516.385.0411  ·  ader.jess@gmail.com  ·  linkedin.com/in/jess-ferretti-324611b', { color: GRAY, size: 18 })],
}));
children.push(new Paragraph({
  spacing: { before: 20, after: 260 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, space: 6, color: 'D5DAE1' } },
  children: [t('NYC Metro / Long Island  ·  Works fully remote, national reach', { color: GRAY, size: 18 })],
}));

// ── Letter ──────────────────────────────────────────────────────────────────
children.push(para('Hello,'));

children.push(para('I will keep this short — the resume covers the history.'));

children.push(para(
  'Twenty-three years in sales, and the part I have never gotten tired of is the beginning: the point ' +
  'where nobody knows yet who the buyer really is, or why the thing matters, or what to say in the first ' +
  'sentence. Working that out with a team, and then watching them go do it without me, is the most ' +
  'satisfying work I know.'
));

children.push(para(
  'That is what I am drawn to — work where the commercial answers are not fully written yet, and people ' +
  'willing to say so out loud. Whether that means building something from nothing or fixing the one part ' +
  'of an engine that is stuck, it is the same job to me, and I have never wanted to do anything else.'
));

children.push(para(
  'You will see on the resume that I am publicly sober and in recovery. I mention it because it is not a ' +
  'footnote. It is where the directness comes from, and it is why the people I work with tell me the truth ' +
  'about their pipeline early enough for it to matter.'
));

children.push(para(
  'I would love to talk, and I would be glad to get specific about your business the moment there is a ' +
  'conversation to have. Thank you for reading this.'
));

children.push(para('Warmly,', { spacing: { before: 240, after: 40 } }));
children.push(para([t('Jess Ferretti', { bold: true })], { spacing: { before: 0, after: 0 } }));

const doc = new Document({
  creator: 'Jess Ferretti',
  title: 'Jess Ferretti — Cover Letter',
  styles: { default: { document: { run: { font: FONT, size: BODY, color: INK } } } },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: {
          top: convertInchesToTwip(0.7),
          bottom: convertInchesToTwip(0.7),
          left: convertInchesToTwip(0.85),
          right: convertInchesToTwip(0.85),
        },
      },
    },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(__dirname + '/Jess-Ferretti-Cover-Letter.docx', buf);
  console.log('wrote Jess-Ferretti-Cover-Letter.docx');
});
