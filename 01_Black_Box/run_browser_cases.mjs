/**
 * Reproducible headless-browser check of the Week 1 cases.
 * Runs only against the isolated app on port 5001. It does not claim to be
 * the manual execution required by the assignment.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require('C:/Users/Admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root = path.dirname(fileURLToPath(import.meta.url));
const evidence = path.join(root, 'evidence');
const screenshots = path.join(evidence, 'browser_screenshots');
const base = 'http://127.0.0.1:5001';
fs.mkdirSync(screenshots, { recursive: true });

const browser = await chromium.launch({
  executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  headless: true,
  args: ['--no-sandbox'],
});

const results = [];
const runStarted = new Date().toISOString();
const testPassword = 'abcdefghi';

function check(ok, message) {
  if (!ok) {
    const error = new Error(message);
    error.testFailure = true;
    throw error;
  }
}

async function newPage() {
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    timezoneId: 'Asia/Singapore',
  });
  const page = await context.newPage();
  page.setDefaultTimeout(7000);
  return { context, page };
}

async function register(page, username, password = testPassword) {
  await page.goto(`${base}/register`);
  await page.locator('input[name="username"]').fill(username);
  await page.locator('input[name="password"]').fill(password);
  await page.getByRole('button', { name: 'Register' }).click();
  return { url: page.url(), error: await page.locator('p.error').allTextContents() };
}

async function login(page, username, password = testPassword) {
  await page.goto(`${base}/login`);
  await page.locator('input[name="username"]').fill(username);
  await page.locator('input[name="password"]').fill(password);
  await page.getByRole('button', { name: 'Log in' }).click();
  return { url: page.url(), error: await page.locator('p.error').allTextContents() };
}

async function logout(page) {
  await page.getByRole('link', { name: 'Log out' }).click();
}

async function createTask(page, { title, description = '', category = '', due = '' }) {
  await page.goto(`${base}/tasks/new`);
  await page.locator('input[name="title"]').fill(title);
  await page.locator('textarea[name="description"]').fill(description);
  if (category) await page.locator('select[name="category_id"]').selectOption({ label: category });
  if (due) await page.locator('input[name="due_date"]').fill(due);
  await page.getByRole('button', { name: 'Create Task' }).click();
}

function taskRow(page, title) {
  return page.locator('tr').filter({ has: page.locator('td.title-cell', { hasText: title }) });
}

async function titles(page) {
  return (await page.locator('td.title-cell').allTextContents()).map((x) => x.trim());
}

async function stat(page, label) {
  return Number((await page.locator('.stat-card').filter({ hasText: label }).locator('.stat-value').innerText()).trim());
}

function localDate(offset = 0) {
  const today = new Date().toLocaleDateString('sv-SE', { timeZone: 'Asia/Singapore' });
  const [year, month, day] = today.split('-').map(Number);
  return new Date(Date.UTC(year, month - 1, day + offset)).toISOString().slice(0, 10);
}

async function fourTaskFixture(page, username) {
  await register(page, username);
  for (const item of [
    { title: 'Work open A', category: 'Work' },
    { title: 'Work done B', category: 'Work' },
    { title: 'Personal open C', category: 'Personal' },
    { title: 'Personal done D', category: 'Personal' },
  ]) await createTask(page, item);
  await taskRow(page, 'Work done B').locator('button.check-btn').click();
  await taskRow(page, 'Personal done D').locator('button.check-btn').click();
}

async function run(id, fn) {
  const { context, page } = await newPage();
  let status = 'Pass';
  let actual = '';
  const shot = path.join(screenshots, `${id}.png`);
  try {
    actual = await fn(page, context);
  } catch (error) {
    status = error.testFailure ? 'Fail' : 'Blocked';
    actual = error.message;
  }
  try {
    await page.screenshot({ path: shot, fullPage: true });
  } catch (error) {
    actual += `; screenshot error: ${error.message}`;
  }
  await context.close();
  results.push({ id, status, actual, screenshot: path.relative(root, shot).replaceAll('\\', '/') });
  console.log(`${id} ${status}: ${actual}`);
  fs.writeFileSync(path.join(evidence, 'browser_results.json'), JSON.stringify({ runStarted, browser: browser.version(), results }, null, 2));
}

// Registration: equivalence partitions and boundaries.
await run('TC-BB-001', async (p) => {
  const r = await register(p, 'abc');
  const nav = await p.locator('.nav-user').innerText();
  check(r.url.endsWith('/') && nav === 'abc', `Expected My Tasks for abc; got ${r.url}, nav=${nav}`);
  return 'Registration opened My Tasks with abc shown in navigation.';
});

await run('TC-BB-002', async (p) => {
  const r = await register(p, 'ab');
  check(r.url.endsWith('/register') && r.error.some((x) => x.includes('3-20')), `Expected username-length error; got ${r.url}, ${r.error}`);
  return `Registration rejected ab: ${r.error.join(' ')}`;
});

await run('TC-BB-003', async (p) => {
  const name = 'abcdefghijklmnopqrst';
  const r = await register(p, name);
  check(r.url.endsWith('/') && (await p.locator('.nav-user').innerText()) === name, `Expected 20-character name accepted; got ${r.url}, ${r.error}`);
  return '20-character username accepted.';
});

await run('TC-BB-004', async (p) => {
  const r = await register(p, 'abcdefghijklmnopqrstu');
  check(r.url.endsWith('/register') && r.error.some((x) => x.includes('3-20')), `Expected 21-character name rejected; got ${r.url}, ${r.error}`);
  return `21-character username rejected: ${r.error.join(' ')}`;
});

await run('TC-BB-005', async (p) => {
  const r = await register(p, 'abc-1');
  check(r.url.endsWith('/register') && r.error.length > 0, `Expected invalid-character error; got ${r.url}`);
  return `Username with hyphen rejected: ${r.error.join(' ')}`;
});

await run('TC-BB-006', async (p) => {
  const r = await register(p, 'pw7user', 'abcdefg');
  check(r.url.endsWith('/register') && r.error.some((x) => x.includes('8')), `Expected 7-character password rejected; got ${r.url}, ${r.error}`);
  return `7-character password rejected: ${r.error.join(' ')}`;
});

await run('TC-BB-007', async (p) => {
  const r = await register(p, 'pw8user', 'abcdefgh');
  check(r.url.endsWith('/'), `Expected 8-character password accepted; got ${r.url}, ${r.error.join(' ')}`);
  return '8-character password accepted.';
});

// Authentication and access.
await run('TC-BB-008', async (p) => {
  await register(p, 'login_user');
  await logout(p);
  const r = await login(p, 'login_user');
  check(r.url.endsWith('/') && (await p.locator('.nav-user').innerText()) === 'login_user', `Expected login success; got ${r.url}, ${r.error}`);
  return 'Correct credentials opened My Tasks under login_user.';
});

await run('TC-BB-009', async (p) => {
  await register(p, 'wrong_pw_user');
  await logout(p);
  const r = await login(p, 'wrong_pw_user', 'wrongpass');
  check(r.url.endsWith('/login') && r.error.some((x) => x.includes('Invalid')), `Expected login error; got ${r.url}, ${r.error}`);
  return `Wrong password rejected: ${r.error.join(' ')}`;
});

await run('TC-BB-010', async (p) => {
  await register(p, 'logout_user');
  await createTask(p, { title: 'Private before logout' });
  await logout(p);
  await p.goto(`${base}/`);
  check(p.url().endsWith('/login') && !(await p.content()).includes('Private before logout'), `Protected page accessible after logout at ${p.url()}`);
  return 'Logout cleared access; direct visit to / redirected to Login.';
});

// Task lifecycle.
await run('TC-BB-011', async (p) => {
  await register(p, 'create_full');
  await createTask(p, { title: 'Submit lab', description: 'Draft report', category: 'Work', due: localDate(3) });
  check((await titles(p)).includes('Submit lab'), 'New task title missing from task list.');
  check((await taskRow(p, 'Submit lab').innerText()).includes('Work'), 'Work category missing from list.');
  await taskRow(p, 'Submit lab').getByRole('link', { name: 'Edit' }).click();
  const description = await p.locator('textarea[name="description"]').inputValue();
  const due = await p.locator('input[name="due_date"]').inputValue();
  check(description === 'Draft report' && due === localDate(3), `Saved form differed: description=${description}, due=${due}`);
  return 'Task saved; title/category visible and description/due date persisted in edit form.';
});

await run('TC-BB-012', async (p) => {
  await register(p, 'create_undated');
  await createTask(p, { title: 'Undated task' });
  const urgency = (await taskRow(p, 'Undated task').locator('.badge').innerText()).trim();
  check(urgency === 'No due date', `Expected No due date, got ${urgency}`);
  return 'Task without optional fields saved; urgency No due date.';
});

await run('TC-BB-013', async (p) => {
  await register(p, 'empty_title');
  await p.goto(`${base}/tasks/new`);
  await p.getByRole('button', { name: 'Create Task' }).click();
  const missing = await p.locator('input[name="title"]').evaluate((el) => el.validity.valueMissing);
  check(p.url().endsWith('/tasks/new') && missing, `Browser did not block empty title; at ${p.url()}`);
  return 'Browser required-field validation blocked an empty title.';
});

await run('TC-BB-014', async (p) => {
  await register(p, 'spaces_title');
  await p.goto(`${base}/tasks/new`);
  await p.locator('input[name="title"]').fill('   ');
  await p.getByRole('button', { name: 'Create Task' }).click();
  const rowCount = await p.locator('td.title-cell').count();
  const errorText = await p.locator('p.error').allTextContents();
  check(p.url().endsWith('/tasks/new') && rowCount === 0 && errorText.length > 0,
    `Whitespace title was accepted: redirected to ${p.url()}, task rows=${rowCount}, error=${errorText.join(' ')}`);
  return 'Whitespace-only title rejected with a validation message.';
});

await run('TC-BB-015', async (p) => {
  await register(p, 'edit_user');
  await createTask(p, { title: 'First original' });
  await createTask(p, { title: 'Second untouched' });
  await taskRow(p, 'First original').getByRole('link', { name: 'Edit' }).click();
  await p.locator('input[name="title"]').fill('Updated lab');
  await p.locator('select[name="category_id"]').selectOption({ label: 'Study' });
  await p.locator('input[name="due_date"]').fill(localDate(2));
  await p.getByRole('button', { name: 'Save Changes' }).click();
  const all = await titles(p);
  check(all.includes('Updated lab') && all.includes('Second untouched') && !all.includes('First original'), `Unexpected titles after edit: ${all}`);
  check((await taskRow(p, 'Updated lab').innerText()).includes('Study'), 'Updated category missing.');
  return 'Selected task changed title/category/due date; second task stayed unchanged.';
});

await run('TC-BB-016', async (p) => {
  await register(p, 'toggle_user');
  await createTask(p, { title: 'Toggle me' });
  await taskRow(p, 'Toggle me').locator('button.check-btn').click();
  check((await taskRow(p, 'Toggle me').getAttribute('class')).includes('done'), 'Task did not become done.');
  await p.goto(`${base}/dashboard`);
  const doneOpen = await stat(p, 'Open');
  const doneRecent = await stat(p, 'Completed (last 7 days)');
  await p.screenshot({ path: path.join(screenshots, 'TC-BB-016-done.png'), fullPage: true });
  await p.goto(`${base}/`);
  await taskRow(p, 'Toggle me').locator('button.check-btn').click();
  await p.goto(`${base}/dashboard`);
  const reopenedOpen = await stat(p, 'Open');
  const reopenedRecent = await stat(p, 'Completed (last 7 days)');
  check(doneOpen === 0 && doneRecent === 1 && reopenedOpen === 1 && reopenedRecent === 0,
    `Counts after done/reopen: open ${doneOpen}/${reopenedOpen}, completed ${doneRecent}/${reopenedRecent}`);
  return 'Open -> done -> open; dashboard open 0 -> 1 and recent completion 1 -> 0.';
});

await run('TC-BB-017', async (p) => {
  await register(p, 'delete_user');
  await createTask(p, { title: 'Delete first' });
  await createTask(p, { title: 'Keep second' });
  p.once('dialog', (dialog) => dialog.accept());
  await taskRow(p, 'Delete first').getByRole('button', { name: 'Delete' }).click();
  const all = await titles(p);
  await p.goto(`${base}/dashboard`);
  const total = await stat(p, 'Total Tasks');
  check(!all.includes('Delete first') && all.includes('Keep second') && total === 1,
    `Delete outcome titles=${all}, dashboard total=${total}`);
  return 'Selected task deleted; other task remained; total became 1.';
});

await run('TC-BB-018', async (p) => {
  await register(p, 'owner_a');
  await createTask(p, { title: 'Owned by A' });
  const editUrl = await taskRow(p, 'Owned by A').getByRole('link', { name: 'Edit' }).getAttribute('href');
  await logout(p);
  const { context: contextB, page: pageB } = await newPage();
  try {
    await register(pageB, 'owner_b');
    const visibleB = await titles(pageB);
    await pageB.goto(`${base}${editUrl}`);
    check(!visibleB.includes('Owned by A') && pageB.url().endsWith('/'),
      `B saw A's task or edit form: titles=${visibleB}, url=${pageB.url()}`);
    await pageB.screenshot({ path: path.join(screenshots, 'TC-BB-018-account-B.png'), fullPage: true });
  } finally {
    await contextB.close();
  }
  await login(p, 'owner_a');
  check((await titles(p)).includes('Owned by A'), 'A task missing or changed after B attempted edit.');
  return 'B could not list or edit A task; A still saw it after signing back in.';
});

// Due-date boundaries.
for (const [number, offset, expected] of [
  [19, -1, 'Overdue'], [20, 0, 'Due Today'], [21, 1, 'Due Soon'],
  [22, 2, 'Due Soon'], [23, 3, 'Upcoming'],
]) {
  const id = `TC-BB-${String(number).padStart(3, '0')}`;
  await run(id, async (p) => {
    await register(p, `due_user_${number}`);
    const due = localDate(offset);
    await createTask(p, { title: `Date boundary ${number}`, due });
    const urgency = (await taskRow(p, `Date boundary ${number}`).locator('.badge').innerText()).trim();
    check(urgency === expected, `Due ${due}: expected ${expected}, observed ${urgency}`);
    return `Due ${due}: urgency ${urgency}.`;
  });
}

// Decision table, search, and dashboard.
for (const [number, category, status, expected] of [
  [24, 'Work', 'open', ['Work open A']],
  [25, 'Work', 'done', ['Work done B']],
  [26, 'Personal', 'open', ['Personal open C']],
  [27, '', 'done', ['Work done B', 'Personal done D']],
]) {
  const id = `TC-BB-${String(number).padStart(3, '0')}`;
  await run(id, async (p) => {
    await fourTaskFixture(p, `filter_user_${number}`);
    if (category) {
      await Promise.all([
        p.waitForURL((url) => url.searchParams.get('category') === category),
        p.locator('select[name="category"]').selectOption({ label: category }),
      ]);
    }
    await Promise.all([
      p.waitForURL((url) => url.searchParams.get('status') === status),
      p.locator('select[name="status"]').selectOption(status),
    ]);
    const observed = await titles(p);
    check(JSON.stringify([...observed].sort()) === JSON.stringify([...expected].sort()),
      `Expected titles ${expected.join(', ')}, observed ${observed.join(', ')}`);
    return `Category=${category || 'All'}, status=${status}; visible: ${observed.join(', ')}.`;
  });
}

await run('TC-BB-028', async (p) => {
  await fourTaskFixture(p, 'search_user');
  await p.locator('input[name="q"]').fill('Personal');
  await p.getByRole('button', { name: 'Filter' }).click();
  const observed = await titles(p);
  check(JSON.stringify([...observed].sort()) === JSON.stringify(['Personal open C', 'Personal done D'].sort()),
    `Search Personal returned ${observed.join(', ')}`);
  return `Search Personal returned ${observed.join(', ')} only.`;
});

await run('TC-BB-029', async (p) => {
  await fourTaskFixture(p, 'dashboard_user');
  await p.goto(`${base}/dashboard`);
  const observed = {
    total: await stat(p, 'Total Tasks'), open: await stat(p, 'Open'),
    overdue: await stat(p, 'Overdue'), soon: await stat(p, 'Due Soon'),
    completed: await stat(p, 'Completed (last 7 days)'),
  };
  check(JSON.stringify(observed) === JSON.stringify({ total: 4, open: 2, overdue: 0, soon: 0, completed: 2 }),
    `Dashboard counts: ${JSON.stringify(observed)}`);
  return `Dashboard counts ${JSON.stringify(observed)}.`;
});

await browser.close();

const counts = Object.fromEntries(['Pass', 'Fail', 'Blocked'].map((s) => [s, results.filter((r) => r.status === s).length]));
// Structured results and screenshots are saved per case in evidence/.
console.log(`SUMMARY ${JSON.stringify(counts)}`);
