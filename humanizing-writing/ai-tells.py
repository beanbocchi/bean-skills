#!/usr/bin/env python3
"""Flag phrases and formatting habits typical of machine-written prose.

Usage:
  ai-tells.py FILE [FILE ...]      flag every hit, print a summary, exit 1 on any hit
  ai-tells.py --stats FILE ...     also print structural stats (words, bold, headings, copula rate)
  ai-tells.py -                    read the draft from stdin

Every hit needs a human read: "underscore" can be a character, "highlight" can be
a marker pen, "landscape" can be a page orientation. The script finds candidates;
the writer decides.
"""
import re
import sys

W = r"\b"

# (category, pattern). Patterns are matched case-insensitively, one line at a time.
RULES = [
    # --- AI vocabulary: the documented over-used words -----------------------
    ("vocab", r"\badditionally\b"),
    ("vocab", r"\balign(s|ed|ing)? with\b"),
    ("vocab", r"\bboast(s|ed|ing)?\b"),
    ("vocab", r"\bbolster\w*"),
    ("vocab", r"\bcrucial(ly)?\b"),
    ("vocab", r"\bdeep[- ]dive\b"),
    ("vocab", r"\bdelv(e|es|ed|ing)\b"),
    ("vocab", r"\bemphasi[sz](e|es|ed|ing)\b"),
    ("vocab", r"\benduring\b"),
    ("vocab", r"\benhanc(e|es|ed|ing|ement|ements)\b"),
    ("vocab", r"\bfoster(s|ed|ing)?\b"),
    ("vocab", r"\bgarner(s|ed|ing)?\b"),
    ("vocab", r"\bhighlight(s|ed|ing)?\b"),
    ("vocab", r"\binterplay\b"),
    ("vocab", r"\bintrica(te|cies|cy)\b"),
    ("vocab", r"\bkey (role|part|aspect|component|feature|factor|element|player|driver|takeaway|insight|consideration|benefit|advantage|point|area|piece|differentiator|challenge|strength|theme|step|question|decision|reason|goal|priorit\w+|pillar)s?\b"),
    ("vocab", r"\b(digital|competitive|tech\w*|business|market|regulatory|current|evolving|changing|ai|data|security|threat|media|economic|political|cultural|broader|enterprise|vendor|tooling|it) landscape\b"),
    ("vocab", r"\blandscape of\b"),
    ("vocab", r"\bmeticulous(ly)?\b"),
    ("vocab", r"\bpivotal\b"),
    ("vocab", r"\brobust(ly|ness)?\b"),
    ("vocab", r"\bshowcas(e|es|ed|ing)\b"),
    ("vocab", r"\btapestry\b"),
    ("vocab", r"\btestament\b"),
    ("vocab", r"\bunderscor(e|es|ed|ing)\b"),
    ("vocab", r"\bvaluable\b"),
    ("vocab", r"\bvibrant\b"),
    ("vocab", r"\bseamless(ly)?\b"),
    ("vocab", r"\bleverag(e|es|ed|ing)\b"),
    ("vocab", r"\bstreamlin(e|es|ed|ing)\b"),
    ("vocab", r"\bcomprehensive(ly)?\b"),
    ("vocab", r"\bholistic(ally)?\b"),
    ("vocab", r"\bcutting[- ]edge\b"),
    ("vocab", r"\bstate[- ]of[- ]the[- ]art\b"),
    ("vocab", r"\bgame[- ]?chang\w+"),
    ("vocab", r"\bgroundbreaking\b"),
    ("vocab", r"\brenowned\b"),
    ("vocab", r"\bnestled\b"),
    ("vocab", r"\bin the heart of\b"),
    ("vocab", r"\bdiverse (array|range|set)\b"),
    ("vocab", r"\bprofound(ly)?\b"),
    ("vocab", r"\bever[- ](evolving|changing|growing)\b"),
    ("vocab", r"\bempower(s|ed|ing|ment)?\b"),
    ("vocab", r"\bunlock(s|ed|ing)? (the |its |their |your |new )?(full )?(potential|value|insights?|possibilities|power|capabilities)\b"),
    ("vocab", r"\bnavigat(e|es|ing) (the )?(complex\w*|landscape|challenges|nuances|intricacies)\b"),
    ("vocab", r"\b(the|a|new|whole|entire|different|digital|political) realm of\b"),
    ("vocab", r"\bparadigm\b"),
    ("vocab", r"\bsynerg\w+"),
    ("vocab", r"\butili[sz](e|es|ed|ing|ation)\b"),
    ("vocab", r"\bfacilitat(e|es|ed|ing)\b"),
    ("vocab", r"\bnotably\b"),
    ("vocab", r"\bmoreover\b"),
    ("vocab", r"\bfurthermore\b"),
    ("vocab", r"\bin today'?s (fast[- ]paced|digital|rapidly|ever[- ]\w+|world|landscape|competitive)\b"),
    ("vocab", r"\bat its core\b"),
    ("vocab", r"\bwhen it comes to\b"),
    ("vocab", r"\ba wide range of\b"),
    ("vocab", r"\btransformative\b"),
    ("vocab", r"\bjourney\b"),
    ("vocab", r"\bbest[- ]in[- ]class\b"),
    ("vocab", r"\bworld[- ]class\b"),
    ("vocab", r"\bfirst[- ]class\b"),
    ("vocab", r"\bpav(e|es|ed|ing) the way\b"),
    ("vocab", r"\bthe (missing|final) piece\b"),
    ("vocab", r"\b(true|real) (data )?sovereignty\b"),
    ("vocab", r"\bunprecedented\b"),
    ("vocab", r"\bgranular\b"),
    ("vocab", r"\bsingle (pane of glass|source of truth)\b"),
    ("vocab", r"\bfriction(less)?\b"),
    ("vocab", r"\bout of the box\b"),
    ("vocab", r"\bfirst[- ]class citizen\b"),
    ("vocab", r"\bturnkey\b"),
    ("vocab", r"\bbattle[- ]tested\b"),
    ("vocab", r"\bfuture[- ]proof\w*"),
    ("vocab", r"\bpeace of mind\b"),
    ("vocab", r"\bwithout (compromising|sacrificing)\b"),
    ("vocab", r"\bit'?s (all )?about\b"),
    ("vocab", r"\bthe (bottom line|takeaway)\b"),
    ("vocab", r"\bdead simple\b"),
    ("vocab", r"\bsimply put\b"),
    # --- avoidance of is / are / has -----------------------------------------
    ("copula", r"\b(serves|serve|served|serving|stands|stand|stood|functions|function|operates|operate|acts|act) as (a|an|the|its|our|your|their)\b"),
    ("copula", r"\brefers to\b"),
    ("copula", r"\b(represents|represent|marks|mark) (a|an|the) (\w+ )?(shift|step|milestone|departure|change|turning|move|first|significant|major|new)\b"),
    ("copula", r"\bholds the distinction\b"),
    ("copula", r"\b(features|offers|provides|delivers|maintains) (a|an) (\w+ )?(range|set|suite|array|variety|selection|number)\b"),
    # --- puffery: significance, legacy, promotion ------------------------------
    ("puffery", r"\bplay(s|ed|ing)? (a|an) (crucial|pivotal|vital|significant|key|important|central|essential|critical|major|fundamental|instrumental) (role|part)\b"),
    ("puffery", r"\b(is|are|stands as|serves as|remains) a (testament|reminder)\b"),
    ("puffery", r"\bunderscor\w+ (the |its )?(importance|significance|need|value|commitment)\b"),
    ("puffery", r"\breflects? (a |the )?broader\b"),
    ("puffery", r"\bsetting the stage\b"),
    ("puffery", r"\b(key )?turning point\b"),
    ("puffery", r"\bindelible mark\b"),
    ("puffery", r"\bdeeply rooted\b"),
    ("puffery", r"\b(enduring|lasting|ongoing) (legacy|impact|influence|significance)\b"),
    ("puffery", r"\bfocal point\b"),
    ("puffery", r"\bcommitment to (excellence|quality|innovation|transparency|security|accountability|customers?)\b"),
    ("puffery", r"\b(a|the) new era\b"),
    ("puffery", r"\bredefin(e|es|ed|ing)\b"),
    ("puffery", r"\brevolutioni[sz]\w+"),
    ("puffery", r"\bshap(e|es|ed|ing) the (future|way|landscape|industry)\b"),
    ("puffery", r"\bcontributing to the\b"),
    ("puffery", r"\bactive (social media )?presence\b"),
    ("puffery", r"\bindependent coverage\b"),
    ("puffery", r"\b(trade|industry|leading) (publications?|outlets?|experts?)\b"),
    ("puffery", r"\bmission[- ]critical\b"),
    ("puffery", r"\benterprise[- ]grade\b"),
    ("puffery", r"\bproduction[- ]grade\b"),
    ("puffery", r"\bindustry[- ]leading\b"),
    ("puffery", r"\bnext[- ]generation\b"),
    ("puffery", r"\bpurpose[- ]built\b"),
    ("puffery", r"\bwith confidence\b"),
    ("puffery", r"\bat scale\b"),
    ("puffery", r"\bthe (right|smart|clear) choice\b"),
    ("puffery", r"\b(truly|genuinely) (unique|innovative|transformative|governed|secure)\b"),
    ("puffery", r"\bno (more|longer) (need to|worrying|guessing|surprises)\b"),
    # --- superficial analysis: trailing participle clause ----------------------
    ("participle", r",\s+(highlighting|underscoring|emphasi[sz]ing|ensuring|reflecting|symboli[sz]ing|fostering|encompassing|enhancing|showcasing|demonstrating|signal(l)?ing|cementing|solidifying|paving|positioning|reinforcing|allowing|enabling|making it|giving|providing|offering|helping|keeping|leaving|creating|contributing|marking|illustrating|reaffirming|guaranteeing|empowering|streamlining|unlocking|driving|shaping|ultimately)\b"),
    # --- weasel attribution ----------------------------------------------------
    ("weasel", r"\b(experts|observers|critics|scholars|analysts|researchers|practitioners|industry (reports|leaders|analysts)|many (people|teams|organi[sz]ations|enterprises)|some (critics|argue)|it is (widely|generally|commonly))\b"),
    ("weasel", r"\bwidely (regarded|recognized|recognised|considered|seen|accepted|adopted)\b"),
    ("weasel", r"\bstudies (show|suggest|have shown)\b"),
    ("weasel", r"\bit'?s no secret\b"),
    ("weasel", r"\b(as|since) (we|you) all know\b"),
    # --- negative parallelism --------------------------------------------------
    ("contrast", r"\bnot (just|only|merely|simply|about)\b.{1,80}\b(but|it'?s|it is|rather)\b"),
    ("contrast", r"\b(it|this|that|which) (is|was|isn'?t|wasn'?t) not\b.{1,60}\b(but|it'?s|it is|rather)\b"),
    ("contrast", r"\bisn'?t (just|only|about|a|an)\b.{1,60}\b(it'?s|but)\b"),
    ("contrast", r"\bno \w+, no \w+, (just|only)\b"),
    ("contrast", r"\binstead of (just|simply|merely)\b"),
    ("contrast", r"\b(more|less) than (just|simply|merely) (a|an)\b"),
    # --- vague connection ------------------------------------------------------
    ("connection", r"\b(in connection (with|to)|associated with|connected (to|with)|in association with|tied to|linked to)\b"),
    # --- reader-facing chatter, disclaimers, summaries -------------------------
    ("chatter", r"\b(i hope this helps|hope (this|that) helps|certainly!?|of course!?|you'?re absolutely right|absolutely!|great question|good question|would you like|let me know|feel free to|happy (coding|editing|building|hacking|testing)|don'?t hesitate|please note that|as requested|as mentioned|as you can see|here'?s (a|an|the|how|what|why)|let'?s (dive|get started|take a look|explore|break)|in this (article|post|guide|section),? we)\b"),
    ("chatter", r"^\s*(in summary|in conclusion|overall|to summari[sz]e|to sum up|to conclude|all in all|ultimately|at the end of the day|in short|in essence|essentially|the bottom line)\b"),
    ("chatter", r"\b(it'?s|it is) (also )?(important|worth|crucial|essential|vital|helpful) (to )?(note|noting|remember|mention|consider|point out|understand|keep in mind)\b"),
    ("chatter", r"\bworth (noting|mentioning|remembering|pointing out)\b"),
    ("chatter", r"\bkeep in mind\b"),
    ("chatter", r"\bas an ai\b"),
    ("chatter", r"\bas of my (last|latest) (knowledge|training)\b"),
    ("chatter", r"\b(while|although) (specific )?(details|information) (are|is) (limited|scarce|not (widely )?available)\b"),
    ("chatter", r"\bbased on (the )?available information\b"),
    ("chatter", r"\bin the provided (sources|context|documents)\b"),
    # --- change-description tells (commit / PR / changelog) --------------------
    ("changelog", r"\bwhile (preserving|maintaining|retaining|keeping|ensuring)\b"),
    ("changelog", r"\b(improv(e|es|ed|ing)|enhanc\w+|refin(e|es|ed|ing)|streamlin\w+|better) (code )?(clarity|readability|maintainability|flow|consistency|robustness|reliability|developer experience|dx|ux|user experience)\b"),
    ("changelog", r"\bfor (better|improved|greater|enhanced) (clarity|readability|maintainability|consistency|reliability|security|performance)\b"),
    ("changelog", r"\bensur(e|es|ed|ing) (that )?(the |all |every )?\w+ (remains?|stays?|continues?|adheres?|complies?|is|are) (consistent|aligned|compliant|correct|intact|backward|unchanged|stable|secure)\b"),
    ("changelog", r"\bcomprehensive (rewrite|update|refactor|overhaul|test)\w*"),
    ("changelog", r"\baimed at\b"),
    ("changelog", r"\bthis (pr|pull request|change|commit|patch) (introduces|aims|enhances|improves|refactors|updates|ensures|adds|makes|brings)\b"),
    ("changelog", r"\b(no|zero) (functional|behavio(u)?ral|breaking) changes?\b"),
    ("changelog", r"\bbackward[s]?[- ]compatib\w+"),
    ("changelog", r"\b(fully|thoroughly|extensively) (tested|verified|validated)\b"),
    ("changelog", r"\ball (existing )?tests (pass|passing|green)\b"),
    ("changelog", r"\bfollow(s|ing)? best practices\b"),
    ("changelog", r"\bbest practices?\b"),
    ("changelog", r"\bclean(er)? (and|,) (more )?(maintainable|readable|consistent)\b"),
    ("changelog", r"\bsingle source of truth\b"),
    ("changelog", r"\bsimplif(y|ies|ied|ying) (the )?(codebase|logic|code|mental model)\b"),
    ("changelog", r"\breduc(e|es|ed|ing) (cognitive load|complexity|boilerplate|surface area)\b"),
    # --- rigid outline formulas ------------------------------------------------
    ("formula", r"\bfaces? (several |numerous |a number of |many |some |significant |ongoing )?challenges\b"),
    ("formula", r"\bdespite (these|its|the|this) (\w+ )?(challenges|limitations|hurdles|obstacles)\b"),
    ("formula", r"^\s*#{1,6}\s*(future (outlook|prospects|directions?|work)|challenges( and \w+)?|conclusion|overview|introduction|key takeaways|final thoughts|summary|awards and recognition|recognition|legacy( and \w+)?|impact( and \w+)?|why (it|this) matters|the bottom line|next steps|closing thoughts|wrapping up|tl;?dr)\s*$"),
    ("formula", r"\blooking ahead\b"),
    ("formula", r"\bmoving forward\b"),
    ("formula", r"\bgoing forward\b"),
    ("formula", r"\bthe (road|path|way) (ahead|forward)\b"),
    # --- punctuation and formatting --------------------------------------------
    ("dash", r"—"),
    ("dash", r"\s–\s"),
    ("dash", r"\w\s--\s\w"),
    ("quotes", r"[“”‘’]"),
    ("emoji", r"[\U0001F000-\U0001FAFF☀-➿⭐⬆⬇✅❌✨‼⁉™ℹ↔-↙↩↪⌚⌛⌨⏏⏩-⏳⏸-⏺Ⓜ▪▫▶◀◻-◾⤴⤵⬅⬛⬜〰〽㊗㊙]"),
    ("bold-list", r"^\s*([-*+•]|\d+[.)])\s+\*\*[^*\n]+\*\*\s*[:：—–-]?"),
    ("bold-list", r"^\s*([-*+•]|\d+[.)])\s+__[^_\n]+__\s*[:：—–-]?"),
    ("rule", r"^\s*(-{3,}|\*{3,}|_{3,})\s*$"),
    ("placeholder", r"\[(your|insert|add|company|name|date|link|url|placeholder|todo|tbd)[^\]]*\]"),
    ("placeholder", r"\((add|insert) [^)]*\)"),
    ("placeholder", r"\b20\d\d-xx-xx\b"),
    ("placeholder", r"\blorem ipsum\b"),
    # --- observed in baseline runs: rhetoric rather than vocabulary -------------
    ("contrast", r"\b(on paper|in theory|nominally)\b[^.]{0,80}\.\s+(in practice|in reality)\b"),
    ("contrast", r"\b(is|was|are) (one|part of the|the obvious|only one|a) (reason|part|piece)[^.]{0,40}\.\s+(the (bigger|larger|real|main|other)|but the) (one|part|reason|point|piece)\b"),
    ("contrast", r"\b(isn'?t|is not|aren'?t|wasn'?t) (there |here |meant |designed |built )?(to|for|about)\b[^.]{1,60}\.\s+(it'?s|it is|they'?re|its purpose is)\b"),
    ("contrast", r"\bstop \w+ing\b[^.]{0,40}\b(and )?start \w+ing\b"),
    ("contrast", r"\b(partly|part) (about|because of|due to)\b[^.]{0,40}\b(mostly|mainly|largely) (about|because)\b"),
    ("contrast", r", (never|not) [a-z]+\.(\s|$)"),
    ("contrast", r"\binstead of (guessing|hoping|assuming|wondering)\b"),
    ("contrast", r"\b(from|by) (the )?(log|data|record)s? (rather than|instead of) (from )?(a )?guess"),
    ("signpost", r"\b(worth (saying|writing about|a word|spelling out|stating)|deserves? (a|its own) (word|mention|paragraph|note)|one (more|last|final) thing\b|(the|that'?s the|this is the) part worth\b|this (page|post|section|document|guide|note) (answers|explains|covers|is about|walks|describes|shows)|that'?s what this (post|page|section) is about|(two|three|four|five) things (stood out|to know|matter|to understand|worth)|the (interesting|important|useful|short|real|honest) (part|answer|bit|point|version) is\b|\bshort answer[:,]|\btl;?dr\b|\bto be (clear|fair|honest)[,:]|\bput (simply|plainly|another way)[,:]|\bin other words[,:]|\bthe point (is|of that|here)\b|\bthat (matters|is the point|is the change)\b|\bthe (upshot|takeaway|result) is\b)"),
    ("signpost", r"^\s*the (first|second|third|fourth) (is|one is)\b"),
    ("concession", r"\b(is|are|was|were|'s) (a )?(fair|real|valid|legitimate|genuine|reasonable|understandable|good) (concern|point|advantage|worry|question|objection|reason|argument)s?\b"),
    ("concession", r"\b(the|your|that) (concern|worry|objection|point|pushback) (is|was) (fair|valid|real|understandable|reasonable|well[- ]taken)\b"),
    ("concession", r"\b(i|we) (understand|get|hear|see) (why|the (concern|worry|appeal|instinct|temptation))\b"),
    ("concession", r"\b(there'?s|there is) (a )?(real|genuine|fair) (case|argument|appeal|advantage) (for|to|in)\b"),
    ("weasel", r"\b(most |many )?people (who work|in (this|the) (industry|field|space)|keep saying|will tell you|tend to agree|generally agree)\b"),
    ("weasel", r"\b(everyone|most people|anyone who has|those who) (agrees?|knows?|will tell you|has seen)\b"),
    ("puffery", r"\b(the direction|where) (we'?re|we are|\w+ is|the industry is|the company is) (building|heading|going)( in| toward| towards)?\b"),
    ("puffery", r"\bwhat we mean by\b"),
    ("puffery", r"\b(is|are) (a )?(fair|good|working|clear|useful) (picture|example|demonstration|illustration|proof) of (what|how|where)\b"),
    ("puffery", r"\bwhat (governed|responsible|modern|real|good) \w+( \w+)? (can|should|will) (achieve|look like|do|be)\b"),
    ("puffery", r"\bresponsible,? (enterprise[- ]grade|governed|scalable) ai\b"),
    ("bold-label", r"^\s*\*\*[^*\n]{2,60}\*\*[.:]?\s+[A-ZÀ-ỿ]"),
    ("heading-slogan", r"^\s*#{2,6}\s+[^\n]*(,| never | not | until | but | yet )[^\n]*$"),
    # --- Vietnamese: the same habits in Vietnamese chat replies ----------------
    ("vi", r"không chỉ\b.{1,80}\bmà còn\b"),
    ("vi", r"\bđóng (một )?vai trò (quan trọng|then chốt|thiết yếu|chủ chốt|trung tâm|cốt lõi|quyết định|không nhỏ)\b"),
    ("vi", r"\b(là )?minh chứng (cho|rõ|sống)\b"),
    ("vi", r"^\s*(tóm lại|nhìn chung|nói tóm lại|kết luận|tổng kết|nói chung|về tổng thể|cuối cùng)[,:]"),
    ("vi", r"\bhy vọng .{0,40}(hữu ích|giúp|có ích)\b"),
    ("vi", r"\b(bạn có muốn (mình|tôi|em)|hãy cho (mình|tôi|em) biết|nếu (bạn )?cần (thêm|gì|hỗ trợ)|cứ (nói|hỏi|bảo)|đừng ngần ngại|mình có thể (giúp|hỗ trợ) (gì )?thêm)\b"),
    ("vi", r"\b(chắc chắn!|tuyệt vời!|câu hỏi (rất )?hay|bạn (hoàn toàn )?(đúng|nói đúng)|đúng rồi!)"),
    ("vi", r"\b(cần|đáng|nên) lưu ý( rằng| là)?\b"),
    ("vi", r"\b(điều|một điểm) (quan trọng|đáng chú ý|cần nhớ|đáng lưu ý)( là| cần)?\b"),
    ("vi", r"\bđáng chú ý (là|rằng)\b"),
    ("vi", r"\b(nâng cao|tối ưu hóa|toàn diện|mạnh mẽ|liền mạch|hệ sinh thái|bức tranh (toàn cảnh|tổng thể|lớn)|bước ngoặt|dấu ấn|tận dụng|nền tảng vững chắc|chìa khóa|đột phá|mang tính cách mạng|làm nổi bật|nhấn mạnh|then chốt|trao quyền|khai phá|kiến tạo|hành trình|trải nghiệm (liền mạch|mượt mà|tuyệt vời)|cảnh quan|góp phần|khẳng định|hướng tới|vươn tới|tiên phong|đẳng cấp|vượt trội)\b"),
    ("vi", r"\b(là )?(lợi thế|điểm yếu|điểm mạnh|lo ngại|băn khoăn|lý do|mối lo|rủi ro) (là )?(thật|có thật|chính đáng|hợp lý|dễ hiểu|thực sự)\b"),
    ("vi", r"\b(mình|tôi|em) hiểu (lý do|vì sao|tại sao|cái|ý|mối lo|băn khoăn)\b"),
    ("vi", r"\bquan trọng (nhất|hơn)( là|,|:)"),
    ("vi", r"^\s*(trả lời ngắn|câu trả lời ngắn|nói ngắn gọn|ngắn gọn|tóm gọn)[:,]"),
    ("vi", r"\bkhông phải (vì|là|do)\b[^.]{1,60}\bmà (là |vì |do )?"),
    ("vi", r"\b(điều|cái|phần|chỗ) (đáng nói|đáng bàn|đáng kể|đáng quan tâm|đáng chú ý|thú vị|quan trọng) (nhất |hơn )?(là|ở đây|nằm ở)\b"),
    ("vi", r"\bmột cách (hiệu quả|toàn diện|liền mạch|mạnh mẽ|tối ưu|linh hoạt|chủ động|rõ ràng|dễ dàng|nhanh chóng|an toàn|minh bạch|bền vững|có hệ thống|có kiểm soát)\b"),
    ("vi", r"\b(về bản chất|nói một cách khác|nói cách khác|nhìn từ góc độ|hơn thế nữa|không những vậy|có thể nói|có thể thấy|rõ ràng là|dễ thấy)\b"),
    ("vi", r"\b(giải pháp|nền tảng|hệ thống|kiến trúc) (toàn diện|mạnh mẽ|hiện đại|tối ưu|linh hoạt|bền vững|đáng tin cậy|hàng đầu)\b"),
    ("vi", r"\b(đảm bảo|bảo đảm) (rằng|tính|sự|việc)?\b"),
    ("vi", r"\b(cho phép|giúp) (bạn|người dùng|đội ngũ|doanh nghiệp|tổ chức) (dễ dàng|nhanh chóng|linh hoạt|chủ động)\b"),
]

COMPILED = [(cat, re.compile(pat, re.IGNORECASE | re.UNICODE)) for cat, pat in RULES]

HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
SMALL = {"a", "an", "the", "of", "and", "or", "for", "to", "in", "on", "with", "at", "by", "vs", "via", "as", "from", "into", "per", "nor", "but", "is", "are", "be"}
BOLD = re.compile(r"\*\*[^*\n]+\*\*|__[^_\n]+__")
BULLET = re.compile(r"^\s*([-*+•]|\d+[.)])\s+")
WORD = re.compile(r"[A-Za-zÀ-ɏḀ-ỿ']+")
COPULA = re.compile(r"\b(is|are|was|were|has|have|had)\b", re.IGNORECASE)
SENTENCE_END = re.compile(r"[.!?](\s|$)")
OPENERS = re.compile(r"^\s*(additionally|moreover|furthermore|notably|importantly|crucially|interestingly|ultimately|overall|however|in addition)\b[,:]?", re.IGNORECASE)


def title_case_heading(line):
    m = HEADING.match(line)
    if not m:
        return None
    if re.match(r"^\s{0,3}#\s", line):
        return None  # an H1 is usually a name; names are capitalised
    text = m.group(1)
    if text.startswith("`") and text.endswith("`"):
        return None
    words = [w for w in re.split(r"\s+", text) if re.search(r"[A-Za-z]", w)]
    content = [w for w in words if w.lower() not in SMALL]
    if len(content) < 3:
        return None
    if all(w[0].isupper() for w in content) and not all(w.isupper() for w in content):
        return text
    return None


def scan(name, text):
    hits = []
    lines = text.splitlines()
    in_code = False
    in_front = bool(lines) and lines[0].strip() == "---"
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if in_front:
            if i > 1 and stripped == "---":
                in_front = False
            continue  # frontmatter keys are not prose
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for cat, rx in COMPILED:
            for m in rx.finditer(line):
                hits.append((name, i, cat, m.group(0), line))
        tc = title_case_heading(line)
        if tc:
            hits.append((name, i, "title-case", tc, line))
        closer = closer_sentence(line)
        if closer:
            hits.append((name, i, "closer", closer, line))
    return hits, lines


def closer_sentence(line, max_words=8):
    """Final sentence of a multi-sentence paragraph when it is short and carries no number or code: a slogan-closer candidate."""
    para = line.strip()
    if not para or para.startswith("#") or BULLET.match(para) or para.startswith("|") or para.startswith("```"):
        return None
    sentences = [x.strip() for x in re.split(r"(?<=[.!?])\s+", para) if x.strip()]
    if len(sentences) < 2:
        return None
    last = sentences[-1]
    if len(last.split()) <= max_words and not re.search(r"[0-9`]", last) and last.endswith("."):
        return last
    return None


def stats(lines):
    text = "\n".join(l for l in lines if not l.strip().startswith("```"))
    words = WORD.findall(text)
    n_words = len(words)
    n_sent = max(1, len(SENTENCE_END.findall(text)))
    bold = len(BOLD.findall(text))
    headings = sum(1 for l in lines if HEADING.match(l))
    bullets = sum(1 for l in lines if BULLET.match(l))
    copula = len(COPULA.findall(text))
    openers = sum(1 for l in lines if OPENERS.match(l))
    em = text.count("—")
    consequence = len(re.findall(r",\s+(so|so that|which means|meaning|ensuring)\b", text, re.IGNORECASE))
    closers = sum(1 for l in lines if closer_sentence(l))
    return {
        "words": n_words,
        "sentences": n_sent,
        "avg_sentence_words": round(n_words / n_sent, 1),
        "headings": headings,
        "bullets": bullets,
        "bold_spans": bold,
        "em_dashes": em,
        "copula_per_100w": round(100 * copula / n_words, 1) if n_words else 0,
        "transition_openers": openers,
        "consequence_clauses": consequence,
        "short_closers": closers,
    }


def excerpt(line, needle, width=110):
    line = line.strip()
    if len(line) <= width:
        return line
    pos = line.lower().find(needle.lower())
    start = max(0, pos - width // 3)
    return ("..." if start else "") + line[start:start + width] + ("..." if start + width < len(line) else "")


def main(argv):
    want_stats = "--stats" in argv
    paths = [a for a in argv if a != "--stats"]
    if not paths:
        print(__doc__)
        return 2
    total = 0
    per_cat = {}
    for path in paths:
        if path == "-":
            text, name = sys.stdin.read(), "<stdin>"
        else:
            with open(path, encoding="utf-8") as f:
                text, name = f.read(), path
        hits, lines = scan(name, text)
        for name_, i, cat, matched, line in hits:
            per_cat[cat] = per_cat.get(cat, 0) + 1
            print(f"{name_}:{i} [{cat}] {matched!r} :: {excerpt(line, matched)}")
        total += len(hits)
        if want_stats:
            s = stats(lines)
            density = round(100 * len(hits) / s["words"], 1) if s["words"] else 0
            print(f"-- {name}: {len(hits)} hits, {density} per 100 words; " + ", ".join(f"{k}={v}" for k, v in s.items()))
    if per_cat:
        summary = ", ".join(f"{k}={v}" for k, v in sorted(per_cat.items(), key=lambda kv: -kv[1]))
        print(f"== {total} hits: {summary}")
    else:
        print("== 0 hits")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
