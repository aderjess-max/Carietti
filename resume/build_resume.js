// Builds resume.docx from the content in resume.md (kept in sync by hand).
// Run: node build_resume.js
const {
  Document, Packer, Paragraph, TextRun, AlignmentType,
  BorderStyle, LevelFormat, convertInchesToTwip, Tab, TabStopType,
} = require('docx');
const fs = require('fs');

const INK   = '0F1319';
const GREEN = '1F8A65';   // darkened from #37B98A so it stays legible in print
const GRAY  = '5A6472';
const FONT  = 'Calibri';

const BODY = 19;   // half-points => 9.5pt
const SMALL = 18;

// Letter width minus both margins — where the right-aligned date column sits.
const TEXT_WIDTH = 12240 - 2 * convertInchesToTwip(0.62);

const p = (opts) => new Paragraph(opts);
const t = (text, o = {}) => new TextRun({ text, font: FONT, color: INK, size: BODY, ...o });

// ── Section header: uppercase, green, hairline rule beneath ────────────────
const section = (label) => p({
  spacing: { before: 260, after: 130 },
  keepNext: true,
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, space: 4, color: GREEN } },
  children: [t(label.toUpperCase(), { bold: true, color: GREEN, size: SMALL, characterSpacing: 30 })],
});

// ── Role header: "Company — Title" left, dates right on the same line ──────
const role = (company, title, dates) => p({
  spacing: { before: 230, after: 0 },
  keepNext: true, keepLines: true,
  tabStops: [{ type: TabStopType.RIGHT, position: TEXT_WIDTH }],
  children: [
    t(company, { bold: true, size: 21 }),
    t(' — ', { color: GRAY }),
    t(title, { size: 21 }),
    new TextRun({ font: FONT, children: [new Tab()] }),
    t(dates, { color: GRAY, size: SMALL }),
  ],
});

const descriptor = (text) => p({
  spacing: { before: 20, after: 60 },
  keepNext: true,
  children: [t(text, { italics: true, color: GRAY, size: SMALL })],
});

const bullet = (runs) => p({
  numbering: { reference: 'dot', level: 0 },
  spacing: { before: 30, after: 30 },
  children: (Array.isArray(runs) ? runs : [t(runs)]),
});

const body = (runs, o = {}) => p({
  spacing: { before: 60, after: 60 },
  children: (Array.isArray(runs) ? runs : [t(runs)]),
  ...o,
});

const label = (head, rest) => p({
  spacing: { before: 60, after: 60 },
  indent: { left: 0 },
  children: [t(head, { bold: true }), t('  '), t(rest, { color: GRAY })],
});

// ─────────────────────────────────────────────────────────────────────────────
// Two variants off one body of content. `health` is the one to lead with;
// `general` is the same record with the vertical claim lifted out of the
// intro so it can go out for roles and industries beyond digital health.
const VARIANTS = {
  health: {
    file: 'Jess-Ferretti-Resume.docx',
    tagline: 'Fractional VP of Sales  ·  Digital Health',
    lede: 'I help digital health companies build the sales engine they do not have yet.',
    track:
      'Twenty-three years in enterprise sales, quotas carried to $12M, and five consecutive companies selling ' +
      'mental health, substance use, recovery, and specialty pharmacy products to self-insured employers and health ' +
      'plans. I know the buyer — CHROs, Total Rewards leaders, benefits consultants, health plan decision-makers — ' +
      'because I have sold to them from six different seats over eight years.',
    recovery:
      'I am also publicly sober and in recovery. Selling into a category built to treat that condition, it is a ' +
      'commercial credential, not a personal footnote: it is why founders trust the positioning work and why buyers ' +
      'take the meeting.',
    carietti: 'Sales and business development practice serving digital health companies · Remote',
    ferrandino: 'The origin of the construction and trades relationships now driving the highest-need employer segment in workplace substance use',
    sell: [
      ['Categories', 'Digital health · Mental health · Substance use and recovery · Digital therapeutics · Specialty pharmacy · Employee benefits and total rewards'],
      ['Buyers', 'CHROs and Heads of Total Rewards · Benefits and wellbeing leaders · Health plan decision-makers · Benefits consultants and brokers · Self-insured employers, Fortune 100 through 1000'],
      ['Motions', 'Founder-led to first sales team · Enterprise and complex committee sales · Consultant and broker channel · Direct-to-employer'],
    ],
  },
  general: {
    file: 'Jess-Ferretti-Resume-General.docx',
    tagline: 'Enterprise Sales Leader  ·  Go-to-Market & Revenue Growth',
    lede: 'I build the sales engine a company does not have yet, and the team that runs it after.',
    track:
      'Twenty-three years in enterprise sales, quotas carried to $12M, and a $50M territory at the high end. I have ' +
      'built commercial functions from nothing at seed stage and run large, complex ones inside Fortune 100 accounts — ' +
      'across healthcare, automotive, manufacturing, retail, CPG, and employee engagement. The constant is the ' +
      'long-cycle, multi-stakeholder sale and the operating discipline underneath it.',
    recovery:
      'I am also publicly sober and in recovery, and certified in behavioral economics, trauma-informed leadership, ' +
      'and LGBTQIA+ leadership. It is not incidental to the work: it is where the directness comes from, and it is ' +
      'how I build teams that tell the truth about their pipeline.',
    carietti: 'Sales and business development practice for founder-led and early-stage commercial teams · Remote',
    ferrandino: 'Built the construction, facilities, and trades relationships that still open doors two decades later',
    sell: [
      ['Industries', 'Healthcare and digital health · Employee benefits and total rewards · Automotive · Manufacturing · Retail and CPG · Facilities and commercial construction'],
      ['Buyers', 'CHROs and Heads of Total Rewards · Health plan decision-makers · Benefits consultants and brokers · OEM and channel partners · Fortune 100 through 1000, and seed stage'],
      ['Motions', 'Founder-led to first sales team · Enterprise and complex committee sales · Channel and partner · Direct-to-enterprise · Territory and team leadership'],
    ],
  },
};

// ─────────────────────────────────────────────────────────────────────────────
function buildChildren(V) {
const children = [];

// Header block
children.push(p({
  spacing: { after: 0 },
  children: [
    t('Jess Ferretti', { bold: true, size: 40, color: INK }),
    t('   (she/her)', { size: 19, color: GRAY }),
  ],
}));
children.push(p({
  spacing: { before: 40, after: 60 },
  children: [t(V.tagline, { bold: true, color: GREEN, size: 22 })],
}));
children.push(p({
  spacing: { after: 0 },
  children: [t('516.385.0411  ·  ader.jess@gmail.com  ·  linkedin.com/in/jess-ferretti-324611b', { color: GRAY, size: SMALL })],
}));
children.push(p({
  spacing: { before: 20, after: 40 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, space: 6, color: 'D5DAE1' } },
  children: [t('NYC Metro / Long Island  ·  Works fully remote, national reach', { color: GRAY, size: SMALL })],
}));

// ── What I Do ───────────────────────────────────────────────────────────────
children.push(section('What I Do'));
children.push(body([t(V.lede, { bold: true })]));
children.push(body(V.track));
children.push(body(
  'What that looks like depends on the company. Sometimes it is the whole engine — positioning, process, CRM, ' +
  'first hires. Sometimes it is the one piece that is stuck: a narrative that is not landing, a pipeline that ' +
  'will not forecast, a founder who needs someone in the room on the enterprise deals. I would rather start with ' +
  'the real problem than with a package.'
));
children.push(body(V.recovery));

// ── Experience ──────────────────────────────────────────────────────────────
children.push(section('Experience'));

// Carietti
children.push(role('The Carietti Group', 'Co-Founder & Principal, Sales & Business Development', 'March 2026 – Present'));
children.push(descriptor(V.carietti));
children.push(body(
  'I work with founders and early commercial teams at the point where selling has to become a system instead of a ' +
  'set of individual efforts. Engagements are scoped to what the company actually needs — a focused project, an ' +
  'ongoing fractional seat, or a full build through to hiring the leader who takes it over.'
));
children.push(body([t('What I take on:', { bold: true })]));
[
  'ICP definition and market segmentation grounded in where the product actually wins',
  'Sales narrative, pitch, discovery framework, and objection handling',
  'Outbound cadences, email templates, and the messaging library behind them',
  'Sales process, stage definitions, qualification criteria, and forecast discipline',
  'Sales tech stack selection and a CRM stood up, configured, and live — not a recommendation deck',
  'Enablement, ramp, and onboarding for the reps who follow',
  'Recruiting and hiring the VP of Sales who takes it from there',
].forEach((b) => children.push(bullet(b)));
children.push(body([t('How I work:', { bold: true })]));
[
  'Founders work directly with me. No junior associates, no bench, no account manager.',
  'I carry the number myself during the build. The playbook gets written from live pipeline, not from theory.',
  'I would rather scope small and earn the rest than sell a package that does not fit.',
  'The goal is always to make myself unnecessary — to build something that outlasts the engagement.',
].forEach((b) => children.push(bullet(b)));

// Sobrynth
children.push(role('Sobrynth', 'VP of Sales, Fractional', 'May 2026 – Present'));
children.push(descriptor('Workplace substance use disorder benefit sold to self-insured employers · Carietti Group engagement'));
[
  'Own commercial strategy and enterprise pipeline for a workplace SUD benefit selling into self-insured employers, benefits consultants, and brokers',
  'Built the employer segmentation model and identified construction as the priority wedge: the US occupation with the highest drug overdose mortality rate (162.6 per 100k, roughly 3x the average worker), 12% alcohol use disorder against a 7.5% national rate, and 150% higher SUD diagnosis rates than other full-time workers — the highest-need, most underserved employer segment in the country',
  'Translate clinical outcomes into the benefits-economics language a CHRO and a broker actually buy on',
].forEach((b) => children.push(bullet(b)));

// VIVIO
children.push(role('VIVIO Health', 'Sr. Director of Sales', '2026 – Present'));
children.push(descriptor('Specialty drug management for large self-insured employers and health plans · Carietti Group engagement'));
[
  'Sell specialty pharmacy cost management into large self-insured employers, health plans, and their consultant channel',
  'Operate at the most technical end of the benefits sale — pharmacy spend, clinical review, and plan design — where the buying committee is finance, clinical, and HR at the same table',
].forEach((b) => children.push(bullet(b)));

// You Are Accountable
children.push(role('You Are Accountable', 'VP, Business Development & Provider Relations', 'March 2025 – March 2026'));
children.push(descriptor('Seed-stage substance use disorder recovery platform · Remote'));
children.push(body([
  t('The in-house version of what I now do fractionally: a sales function built from nothing at a seed-stage company.', { italics: true }),
]));
[
  'Built the enterprise sales strategy from the ground up, expanding beyond recovery-native buyers into new employer verticals',
  'Opened 60+ new employer opportunities in the first year',
  'Designed and implemented the CRM architecture and sales process from scratch',
  'Established the go-to-market motion across employer, provider, and channel segments',
  'Led and developed the sales team driving cross-industry expansion',
  'Positioned the organization for scalable growth through structured pipeline management and a repeatable enterprise motion',
].forEach((b) => children.push(bullet(b)));

// Koa
children.push(role('Koa Health', 'Head of Enterprise Sales', 'April 2024 – February 2025'));
children.push(descriptor('Digital therapeutics and mental health, sold to employers · Remote'));
[
  'Reported directly to the CRO; drove US sales into employee populations of 2,000+',
  'Made the company’s first-ever US sale, to a large agricultural organization',
  'Evaluated and commercialized dormant IP — crisis prediction tooling, body dysmorphia programming, PTSD digital therapeutics — turning shelved assets into sellable product',
  'Partnered with the C-suite and board to roadmap and prioritize enhancements to already-commercialized products',
  'Built differentiation campaigns with Marketing in a saturated category — clinical efficacy, political stress, and a video series on employee experience of PTSD, substance use, LGBTQIA+ resistance at work, and neurodivergence',
].forEach((b) => children.push(bullet(b)));

// Spring
children.push(role('Spring Health', 'Sr. Director, Strategic Accounts', 'June 2023 – April 2024'));
children.push(descriptor('Mental health, sold to employers and health plans · Remote'));
[
  'Sold into and supported employee populations of 10,000+',
  'Personal pipeline reported at 3x the size of any other rep’s',
  'Created the prospecting process and metrics, then trained the team to execute against them',
  'Built substantial benefits consultant relationships on a working understanding of the benefits and healthcare ecosystem',
  'Events Chair, Sober @ Spring ERG',
].forEach((b) => children.push(bullet(b)));

// BIW
children.push(role('BI WORLDWIDE', 'Sr. Director, Strategy & Innovation', 'March 2018 – June 2023'));
children.push(descriptor('Global employee, channel, and customer engagement agency · Remote'));
children.push(bullet([
  t('Formulated and deployed business transformation across a '),
  t('$12,000,000 client portfolio', { bold: true }),
]));
[
  'Built long-term strategic roadmaps for Fortune 100, 500, and 1,000 clients across sales, customer loyalty, employee engagement, and channel partner engagement',
  'Developed the company’s thought leadership strategy around prospecting',
  'Depth across healthcare, automotive, retail, CPG, and manufacturing',
  'Two-time President’s Club winner; Pacesetter Award, 2019',
].forEach((b) => children.push(bullet(b)));

// DPS
children.push(role('Dealer Product Services (DPS)', 'Sr. Director, New York / East', 'October 2012 – March 2018'));
children.push(descriptor('Automotive dealer management software and workflow · Remote'));
[
  'Managed and grew a $4.5M territory at 10% year over year',
  'Promoted to Sr. Director, East Coast — direct reports and a $50,000,000 territory',
  'Drove direct partnerships with BMW, Mercedes-Benz USA, and Mini Cooper on national strategy',
  'The only woman to achieve President’s Club every single year of her tenure',
].forEach((b) => children.push(bullet(b)));

// Ferrandino
children.push(role('Ferrandino & Son', 'Director of Regional Sales', 'October 2008 – October 2012'));
children.push(descriptor('National commercial general contractor and facility maintenance · Farmingdale, NY'));
[
  'Built the company’s first regionally focused sales team',
  'Grew partnerships with the American Museum of Natural History, MoMA, Union Square Hospitality Group, Hofstra University, and The Intrepid',
  'Took on marketing responsibility in the final year, building the client communication strategy',
  V.ferrandino,
].forEach((b) => children.push(bullet(b)));

// ── Where I Sell ────────────────────────────────────────────────────────────
children.push(section('Where I Sell'));
V.sell.forEach(([head, rest]) => children.push(label(head, rest)));
children.push(label('Build', 'ICP and segmentation · Sales narrative · Outbound cadences · Sales process and forecasting · Sales tech stack and CRM implementation · Enablement and ramp · Hiring VP-level sales leaders'));

// ── Education ───────────────────────────────────────────────────────────────
children.push(section('Education & Certifications'));
children.push(label('Hofstra University', 'BA Business Management · BA Creative Writing'));
children.push(label('Certified in', 'Behavioral Economics · Trauma-Informed Leadership · LGBTQIA+ Leadership'));

// ── Awards ──────────────────────────────────────────────────────────────────
children.push(section('Awards'));
[
  ['President’s Club', '2012, 2013, 2014, 2015, 2016, 2017 · DPS'],
  ['Manager of the Year', '2014, 2017 · DPS'],
  ['Rookie of the Year', '2012 · DPS'],
  ['Pacesetter Award', '2019 · BI WORLDWIDE'],
  ['Keynote Speaker, Thank You Award', '2020 · BI WORLDWIDE'],
  ['The Markswoman Award', '2022 · HiringThing'],
].forEach(([a, b]) => children.push(bullet([t(a, { bold: true }), t('  —  ' + b, { color: GRAY })])));

// ── Personal ────────────────────────────────────────────────────────────────
children.push(section('Personal'));
children.push(body(
  'Born and raised on Long Island. Mom of two girls and a proud member of the LGBTQIA+ community. Performed ' +
  'professional theatre right out of college before deciding to drive change in the corporate world instead — ' +
  'which is still, more or less, the job.'
));

return children;
}

// ─────────────────────────────────────────────────────────────────────────────
const buildDoc = (V) => new Document({
  creator: 'Jess Ferretti',
  title: 'Jess Ferretti — ' + V.tagline.replace(/\s+·\s+/g, ', '),
  numbering: {
    config: [{
      reference: 'dot',
      levels: [{
        level: 0,
        format: LevelFormat.BULLET,
        text: '•',
        alignment: AlignmentType.LEFT,
        style: {
          paragraph: { indent: { left: convertInchesToTwip(0.22), hanging: convertInchesToTwip(0.14) } },
          run: { color: GREEN, font: FONT, size: BODY },
        },
      }],
    }],
  },
  styles: {
    default: {
      document: { run: { font: FONT, size: BODY, color: INK }, paragraph: { spacing: { line: 250 } } },
    },
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: {
          top: convertInchesToTwip(0.5),
          bottom: convertInchesToTwip(0.5),
          left: convertInchesToTwip(0.62),
          right: convertInchesToTwip(0.62),
        },
      },
    },
    children: buildChildren(V),
  }],
});

Object.values(VARIANTS).forEach((V) => {
  Packer.toBuffer(buildDoc(V)).then((buf) => {
    fs.writeFileSync(__dirname + '/' + V.file, buf);
    console.log('wrote ' + V.file);
  });
});
