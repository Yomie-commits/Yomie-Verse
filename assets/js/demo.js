// Interactive demo of the AI Executive Assistant using fictional sample emails.
// Results are pre-written in the same format the real system produces; no real inbox is used.
(function () {
  var root = document.getElementById('demo');
  if (!root) return;

  function day(offset) {
    var d = new Date(); d.setDate(d.getDate() + offset);
    return d.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short' });
  }
  function nextWeekday(target) { // 1 = Monday ... 5 = Friday
    var d = new Date(); var diff = (target - d.getDay() + 7) % 7 || 7; return diff;
  }

  var emails = [
    {
      id: 1, from: 'Wanjiru Kamau', org: 'Client, Savanna Retail', subject: 'Payment page is down – customers can\'t pay',
      preview: 'Hi, since this morning customers get an error at checkout. We are losing sales…',
      body: 'Hi,\n\nSince this morning customers get an error at checkout and cannot complete payment. We are losing sales every hour. Can someone look at this today and confirm by 2pm what is happening?\n\nWanjiru',
      result: {
        priority: 'Critical', category: 'Client Request',
        summary: 'A client\'s checkout page has been failing since this morning and customers cannot pay. They want confirmation by 2pm today.',
        action: 'Get the checkout issue investigated and update the client by 2pm.',
        deadline: 'Today, 14:00', followup: day(0), response: 'Yes', label: 'EA Urgent',
        draft: 'Hi Wanjiru,\n\nThank you for flagging this. I have passed it on as urgent and will update you by 2pm today on [what the team has found / next steps].\n\nBest regards,\n[Your name]'
      }
    },
    {
      id: 2, from: 'David Otieno', org: 'Partner, Lakeview Consulting', subject: 'Q1 planning call – next week?',
      preview: 'Could we have a 45-minute call on Tuesday at 10:00 to plan Q1?…',
      body: 'Hello,\n\nCould we have a 45-minute call next Tuesday at 10:00 to plan Q1 activities? Google Meet works for us.\n\nRegards,\nDavid',
      result: {
        priority: 'High', category: 'Meeting Request',
        summary: 'A partner proposes a 45-minute Q1 planning call next Tuesday at 10:00 on Google Meet.',
        action: 'Confirm whether next Tuesday 10:00 works.', deadline: 'None stated', followup: day(2), response: 'Yes',
        meeting: { title: 'Q1 planning call – Lakeview Consulting', when: day(nextWeekday(2)) + ', 10:00–10:45', where: 'Google Meet', conflict: 'No conflict found' },
        draft: 'Hello David,\n\nThank you for reaching out. [Tuesday at 10:00 works for me / Could we try another time?] I will send a calendar invitation once confirmed.\n\nRegards,\n[Your name]'
      }
    },
    {
      id: 3, from: 'Faith Njeri', org: 'Supplier, Prime Office Supplies', subject: 'Proposal for review by Friday',
      preview: 'Please find attached the draft supply proposal. We need your comments by Friday…',
      body: 'Dear team,\n\nPlease find attached the draft supply proposal for next year. We need your comments by Friday so we can finalise pricing.\n\nKind regards,\nFaith',
      attachment: 'supply-proposal-draft.pdf',
      result: {
        priority: 'High', category: 'Deadline',
        summary: 'A supplier sent a draft supply proposal and needs comments by Friday to finalise pricing.',
        action: 'Review the attached proposal and send comments.', deadline: 'Friday (' + day(nextWeekday(5)) + ')', followup: day(nextWeekday(5)), response: 'Yes',
        attachmentNote: 'Yes: draft supply proposal (PDF)',
        draft: 'Dear Faith,\n\nThank you for sending the draft proposal. I will review it and share comments by Friday.\n\nKind regards,\n[Your name]'
      }
    },
    {
      id: 4, from: 'Weekly Marketing Digest', org: 'newsletter@example-digest.com', subject: '10 trends to watch this month',
      preview: 'This week: growth hacks, social media tips and more…', newsletter: true,
      body: 'This week: growth hacks, social media tips and more. Unsubscribe at any time.'
    },
    {
      id: 5, from: 'Peter Mwangi', org: 'Prospect', subject: 'Question about your rates',
      preview: 'Hi, I saw your services online. What would it cost to set up…',
      body: 'Hi,\n\nI saw your services online. What would it cost to set up email automation for a team of five? Could you share your rates?\n\nThanks,\nPeter',
      result: {
        priority: 'Normal', category: 'Response Needed',
        summary: 'A prospect asks for pricing to set up email automation for a five-person team.',
        action: 'Reply with pricing information.', deadline: 'None stated', followup: day(2), response: 'Yes',
        draft: 'Hi Peter,\n\nThank you for your interest. Pricing depends on your workflow and the tools you use; our packages start at [price]. Could we book a short call to understand your needs? [Suggest times]\n\nBest regards,\n[Your name]'
      }
    },
    {
      id: 6, from: 'Accounts – Mara Logistics', org: 'Vendor', subject: 'Invoice INV-2041 – payment confirmation',
      preview: 'We will confirm receipt of payment by Tuesday…',
      body: 'Hello,\n\nThank you for your payment. Our finance team will confirm receipt of invoice INV-2041 by Tuesday.\n\nAccounts Team',
      result: {
        priority: 'Low', category: 'Follow-up',
        summary: 'The vendor will confirm receipt of payment for invoice INV-2041 by Tuesday.',
        action: 'None', deadline: 'None stated', followup: day(nextWeekday(2)), response: 'No',
        draft: null
      }
    }
  ];

  var processed = {};
  var selected = null;
  var approvals = {};
  var running = false;

  var list = document.getElementById('demo-inbox');
  var detail = document.getElementById('demo-detail');
  var runBtn = document.getElementById('demo-run');
  var resetBtn = document.getElementById('demo-reset');
  var bar = document.getElementById('demo-progress');
  var tabs = root.querySelectorAll('.tab');
  var currentTab = 'email';

  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]; }); }
  function tagClass(p) { return 'tag l-' + p.toLowerCase(); }

  function renderInbox() {
    list.innerHTML = emails.map(function (e) {
      var st = processed[e.id];
      var status = !st ? 'Waiting' : (e.newsletter ? 'Skipped – newsletter (no AI credits used)' : 'Processed · ' + e.result.priority);
      var cls = !st ? '' : (e.newsletter ? 'skip' : 'done');
      return '<button class="inbox-item' + (selected === e.id ? ' active' : '') + '" data-id="' + e.id + '" type="button">' +
        '<strong>' + esc(e.from) + '</strong><span>' + esc(e.subject) + '</span><span>' + esc(e.preview) + '</span>' +
        '<div class="status ' + cls + '">' + esc(status) + '</div></button>';
    }).join('');
  }

  function emailView() {
    var e = emails.filter(function (x) { return x.id === selected; })[0];
    if (!e) return '<div class="empty">Press <b>Run the assistant</b>, then pick an email to see what the AI did with it.</div>';
    var html = '<p style="margin:0;color:var(--muted);font-size:.9rem">From <b>' + esc(e.from) + '</b> · ' + esc(e.org) + '</p>' +
      '<h3 style="margin:.3em 0 .6em">' + esc(e.subject) + '</h3>' +
      '<div class="result wide" style="white-space:pre-line">' + esc(e.body) + (e.attachment ? '\n\n📎 ' + esc(e.attachment) : '') + '</div>';
    if (!processed[e.id]) return html + '<p class="demo-disclaimer">Not processed yet. Press <b>Run the assistant</b>.</p>';
    if (e.newsletter) return html + '<div class="note" style="margin-top:16px"><b>Skipped before AI.</b> Newsletters and promotions are filtered out first, so they never use AI credits or clutter your dashboard.</div>';
    var r = e.result;
    html += '<div class="result-grid">' +
      '<div class="result"><small>Priority</small><span class="' + tagClass(r.priority) + '">' + r.priority + '</span>' + (r.label ? ' <span class="tag l-low">Gmail label: ' + r.label + '</span>' : '') + '</div>' +
      '<div class="result"><small>Category</small>' + esc(r.category) + '</div>' +
      '<div class="result wide"><small>Summary</small>' + esc(r.summary) + '</div>' +
      '<div class="result wide"><small>Required action</small>' + esc(r.action) + '</div>' +
      '<div class="result"><small>Deadline</small>' + esc(r.deadline) + '</div>' +
      '<div class="result"><small>Follow-up date</small>' + esc(r.followup) + '</div>' +
      (r.attachmentNote ? '<div class="result wide"><small>Attachment</small>' + esc(r.attachmentNote) + '</div>' : '') +
      '</div>';
    if (r.draft) {
      html += '<small style="font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)">Reply draft saved in the Gmail thread</small>' +
        '<div class="draft" style="margin-top:6px">' + esc(r.draft) + '</div>' +
        '<p class="demo-disclaimer">Square brackets mark decisions only you can make. The draft is never sent automatically: you edit it and press Send yourself.</p>';
    } else {
      html += '<p class="demo-disclaimer">No reply needed, so no draft was created. A follow-up reminder is set for ' + esc(r.followup) + '.</p>';
    }
    if (r.meeting) {
      html += '<div class="note" style="margin-top:12px"><b>Meeting request detected.</b> Added to the Approvals list – see the <a href="#" data-goto="approvals">Approvals</a> tab.</div>';
    }
    return html;
  }

  function done() { return emails.filter(function (e) { return processed[e.id] && !e.newsletter; }); }

  function dashboardView() {
    var rows = done();
    if (!rows.length) return '<div class="empty">The dashboard fills in as emails are processed.</div>';
    return '<div class="table-wrap"><table><thead><tr><th>From</th><th>Subject</th><th>Priority</th><th>Category</th><th>Required action</th><th>Status</th></tr></thead><tbody>' +
      rows.map(function (e) {
        return '<tr><td>' + esc(e.from) + '</td><td>' + esc(e.subject) + '</td><td><span class="' + tagClass(e.result.priority) + '">' + e.result.priority + '</span></td><td>' + esc(e.result.category) + '</td><td>' + esc(e.result.action) + '</td><td>New</td></tr>';
      }).join('') + '</tbody></table></div><p class="demo-disclaimer" style="padding:0 16px 16px">In the real system this is a Google Sheet you own. You update the Status column as you work.</p>';
  }

  function tasksView() {
    var rows = done().filter(function (e) { return e.result.action !== 'None'; });
    var fu = done();
    if (!fu.length) return '<div class="empty">Tasks and follow-ups appear here after processing.</div>';
    return '<div style="padding:16px 16px 0"><h4 style="margin:0 0 8px">Tasks</h4></div><div class="table-wrap"><table><thead><tr><th>Task</th><th>Priority</th><th>Due</th><th>Status</th></tr></thead><tbody>' +
      rows.map(function (e) { return '<tr><td>' + esc(e.result.action) + '</td><td><span class="' + tagClass(e.result.priority) + '">' + e.result.priority + '</span></td><td>' + esc(e.result.deadline === 'None stated' ? '—' : e.result.deadline) + '</td><td>Open</td></tr>'; }).join('') +
      '</tbody></table></div><div style="padding:16px 16px 0"><h4 style="margin:0 0 8px">Follow-ups</h4></div><div class="table-wrap"><table><thead><tr><th>Conversation</th><th>Contact</th><th>Follow up on</th></tr></thead><tbody>' +
      fu.map(function (e) { return '<tr><td>' + esc(e.subject) + '</td><td>' + esc(e.from) + '</td><td>' + esc(e.result.followup) + '</td></tr>'; }).join('') +
      '</tbody></table></div><p class="demo-disclaimer" style="padding:0 16px 16px">Overdue items are flagged once in the morning briefing, not repeated every day.</p>';
  }

  function approvalsView() {
    var m = done().filter(function (e) { return e.result.meeting; });
    if (!m.length) return '<div class="empty">Meeting requests found in emails wait here for your approval.</div>';
    return m.map(function (e) {
      var mt = e.result.meeting, state = approvals[e.id];
      var actions = state ? '<p style="margin:12px 0 0;font-weight:700;color:' + (state === 'Approved' ? 'var(--success)' : 'var(--muted)') + '">' +
        (state === 'Approved' ? '✓ Approved – the event is added to your Google Calendar at the next scheduled run.' : 'Rejected – nothing is added.') + '</p>'
        : '<div class="approve-bar"><button class="btn btn-primary btn-sm" data-approve="' + e.id + '" type="button">Approve</button><button class="btn btn-outline-dark btn-sm" data-reject="' + e.id + '" type="button">Reject</button></div>';
      return '<div class="demo-body" style="border-bottom:1px solid var(--line)"><h3 style="margin-bottom:.4em">' + esc(mt.title) + '</h3>' +
        '<div class="result-grid"><div class="result"><small>When</small>' + esc(mt.when) + '</div><div class="result"><small>Where</small>' + esc(mt.where) + '</div>' +
        '<div class="result"><small>Requested by</small>' + esc(e.from) + '</div><div class="result"><small>Calendar check</small>' + esc(mt.conflict) + '</div></div>' + actions + '</div>';
    }).join('') + '<p class="demo-disclaimer" style="padding:0 22px 16px">Nothing is sent to the other person. Events are only created after you approve them.</p>';
  }

  function briefingView() {
    var rows = done();
    if (!rows.length) return '<div class="empty">The 7-section morning briefing is generated from the dashboard.</div>';
    var urgent = rows.filter(function (e) { return /Critical|High/.test(e.result.priority); });
    var tasks = rows.filter(function (e) { return e.result.action !== 'None'; });
    var meetings = rows.filter(function (e) { return e.result.meeting; });
    function li(arr, f) { return arr.length ? '<ul>' + arr.map(function (e) { return '<li>' + f(e) + '</li>'; }).join('') + '</ul>' : '<p style="color:var(--muted)">Nothing to report.</p>'; }
    return '<div class="briefing"><p style="color:var(--muted);margin:0">Daily Executive Briefing · ' + day(1) + ' · 07:00</p>' +
      '<h4>1. Important emails received</h4>' + li(rows, function (e) { return '<b>' + e.result.priority + '</b> – ' + esc(e.subject) + ' (' + esc(e.from) + ')'; }) +
      '<h4>2. Critical and high-priority matters</h4>' + li(urgent, function (e) { return esc(e.result.action) + ' <i>Deadline: ' + esc(e.result.deadline) + '</i>'; }) +
      '<h4>3. Outstanding tasks</h4>' + li(tasks, function (e) { return esc(e.result.action); }) +
      '<h4>4. Upcoming deadlines</h4>' + li(rows.filter(function (e) { return e.result.deadline !== 'None stated'; }), function (e) { return esc(e.subject) + ' – ' + esc(e.result.deadline); }) +
      '<h4>5. Meetings today and awaiting approval</h4>' + li(meetings, function (e) { return esc(e.result.meeting.title) + ' – ' + esc(e.result.meeting.when) + (approvals[e.id] ? ' (' + approvals[e.id] + ')' : ' (awaiting your approval)'); }) +
      '<h4>6. Overdue follow-ups</h4><p style="color:var(--muted)">Nothing to report.</p>' +
      '<h4>7. Recommended actions</h4><ul><li>Reply to Wanjiru about the checkout issue before 2pm.</li><li>Approve or reject the Q1 planning call.</li><li>Block time to review the supply proposal before Friday.</li></ul></div>';
  }

  var views = { email: emailView, dashboard: dashboardView, tasks: tasksView, approvals: approvalsView, briefing: briefingView };

  function render() {
    renderInbox();
    detail.innerHTML = '<div class="' + (currentTab === 'email' ? 'demo-body' : '') + '">' + views[currentTab]() + '</div>';
    tabs.forEach(function (t) { t.setAttribute('aria-selected', t.dataset.tab === currentTab ? 'true' : 'false'); });
  }

  function setTab(name) { currentTab = name; render(); }

  tabs.forEach(function (t) { t.addEventListener('click', function () { setTab(t.dataset.tab); }); });

  list.addEventListener('click', function (ev) {
    var b = ev.target.closest('.inbox-item'); if (!b) return;
    selected = Number(b.dataset.id); currentTab = 'email'; render();
  });

  detail.addEventListener('click', function (ev) {
    var a = ev.target.closest('[data-approve],[data-reject],[data-goto]'); if (!a) return;
    ev.preventDefault();
    if (a.dataset.goto) { setTab(a.dataset.goto); return; }
    if (a.dataset.approve) approvals[a.dataset.approve] = 'Approved';
    if (a.dataset.reject) approvals[a.dataset.reject] = 'Rejected';
    render();
  });

  runBtn.addEventListener('click', function () {
    if (running) return;
    running = true; runBtn.disabled = true; runBtn.textContent = 'Processing…';
    var i = 0;
    (function next() {
      if (i >= emails.length) {
        running = false; runBtn.textContent = 'Done ✓'; bar.style.width = '100%';
        if (!selected) selected = 1; render(); return;
      }
      processed[emails[i].id] = true; selected = emails[i].id; i++;
      bar.style.width = Math.round(i / emails.length * 100) + '%';
      render();
      setTimeout(next, 650);
    })();
  });

  resetBtn.addEventListener('click', function () {
    processed = {}; approvals = {}; selected = null; currentTab = 'email'; running = false;
    runBtn.disabled = false; runBtn.textContent = 'Run the assistant'; bar.style.width = '0'; render();
  });

  render();
})();
