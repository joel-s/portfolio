(custom-set-variables
  ;; custom-set-variables was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 '(ange-ftp-try-passive-mode t)
 '(inhibit-startup-screen t)
 '(tool-bar-mode nil))

(custom-set-faces
  ;; custom-set-faces was added by Custom.
  ;; If you edit it by hand, you could mess it up, so be careful.
  ;; Your init file should contain only one such instance.
  ;; If there is more than one, they won't work right.
 )

;; Are we running XEmacs or Emacs?
(defvar running-xemacs (string-match "XEmacs\\|Lucid" emacs-version))

(defvar at-home nil)

(pending-delete-mode +1)

(setq x-select-enable-clipboard t)
(setq interprogram-paste-function 'x-cut-buffer-or-selection-value)
(set-scroll-bar-mode 'right)

;;;=========================================================================
;;; My own functions

(defun reset-frame-size
  "Set the frame size to a pre-defined size."
  (interactive)
  (set-frame-size (selected-frame) 84 72))

;; (reset-frame-size)


(defun range (begin end &optional step)
  (if (null step)
      (setq step 1))
  (cond
   ((zerop step)
    (error "range called with step 0: infinite repetition"))
   ((and (> step 0) (>= begin end))
    nil)
   ((and (< step 0) (<= begin end))
    nil)
   (t
    (cons begin (range (+ begin step) end step)))))

;;--------------------------------------------------------------------------
;; Scrolling functions -- based on Bill Kerr's dogpump scrolling

(defvar microscroll-lines 4
  "Default number of lines for `microscroll-' functions")

(defun microscroll-up (&optional arg)
  "Scroll this buffer `microscroll-lines' lines up.
With prefix argument, scroll that many lines up."
  (interactive)
  (scroll-up microscroll-lines))

(defun microscroll-down ()
  "Scroll this buffer `microscroll-lines' lines down.
With prefix argument, scroll that many lines down."
  (interactive)
  (scroll-down microscroll-lines))


;;--------------------------------------------------------------------------
;; Functions for "cleaning up" regions/documents, in the spirit of tabify
;; and cleanup-backspaces.

(defun cleanup-backspcace-chars (start end)
  "Remove character-backspace sequences in the region.
Called non-interactively, the region is specified by arguments
START and END, rather than by the position of point and mark."
  (interactive "*r")
  ;; Ensure start < end. (Only an issue when called non-interactively.)
  (if (> start end) (let (mid) (setq mid start start end end mid)))
  (save-excursion
    (save-restriction
      (narrow-to-region (point-min) end)
      (goto-char start)
      (while (search-forward "\b" nil t)
          (delete-char -2)))))

(defun cleanup-dos-text ()
  "Remove all control-M characters in the current buffer."
  (interactive)
  (save-excursion
    (while (search-forward "\C-m" nil t)
      (replace-match "" nil t))
    (message "Eliminated Control-M characters")))


;; I spent a couple hours writing the following two functions to clean up
;; whitepace. I revised them in XEmacs on 12 Mar 1998, using the functions
;; tabify and untabify as a model.

(defun cleanup-space (start end)
  "Remove spaces and tabs at the end of each line in the region.
Called non-interactively, the region is specified by arguments
START and END, rather than by the position of point and mark."
  (interactive "*r")
  ;; Ensure start < end. (Only an issue when called non-interactively.)
  (if (> start end) (let (mid) (setq mid start start end end mid)))
  (save-excursion
    (save-restriction
      (narrow-to-region (point-min) end)
      (goto-char start)
      (let ((percent 5))
        (while (re-search-forward "[ \t]+$" nil t)
          (delete-region (match-beginning 0) (point))
          ;; Show progress (copied from untabify.el)
          (if (> (/ (* 100 (- (point) start)) (- (point-max) start))
                 percent)
              (progn
                (message "cleanup-space: %d%% ..." percent)
                (setq percent (+ 5 percent))))))
      (message "cleanup-space: done")))
  nil)

(defun cleanup-space-buffer ()
  "Remove spaces and tabs at the end of each line in the buffer.
Also remove all whitespace from the end of the buffer, replacing it with
a single newline character."
  (interactive "*")
  (cleanup-space (point-min) (point-max))
  (save-excursion
    (save-restriction
      (widen)
      (goto-char (point-max))
      ;; If the last character is a newline, delete all the newlines before
      ;; it; otherwise, add a newline
      (cond
       ((char-equal (preceding-char) ?\n)
        (backward-char)
        (let ((here (point)))           ; from c-electric-delete
          (skip-chars-backward " \t\n")
          (if (/= (point) here)
              (delete-region (point) here))))
       (t
        (insert ?\n)))))
  nil)

(defun cleanup-space-buffer-or-region ()
  "Cleanup space in the region (if it's active) or in the entire buffer.
See `cleanup-space' and `cleanup-space-buffer' for more information."
  (interactive "*")
  (if (region-active-p)
      (cleanup-space (point) (mark))
    (cleanup-space-buffer)))

(defun tabify-indentation (start end)
  "Convert indentation in the region to tabs.

A group of spaces and/or tabs at the beginning of a line is
partially replaced by tabs when this can be done without
changing the column they end at. Called non-interactively, the
region is specified by arguments START and END, rather than by
the position of point and mark. The variable `tab-width'
controls the spacing of tab stops.

This function is identical to tabify except for the ^ in the
regular expression."

  (interactive "r")
  (save-excursion
    (save-restriction
      ;; Include the beginning of the line in the narrowing
      ;; since otherwise it will throw off current-column.
      (goto-char start)
      (beginning-of-line)
      (narrow-to-region (point) end)
      (goto-char start)
      (let ((percent 5))
        (while (re-search-forward "^[ \t][ \t][ \t]*" nil t)
          (let ((column (current-column))
                (indent-tabs-mode t))
            (delete-region (match-beginning 0) (point))
            ;; XEmacs change -- show progress
            (indent-to column)
            (if (> (/ (* 100 (- (point) start)) (- (point-max) start)) percent)
                (progn
                  (message "tabify-indentaton: %d%% ..." percent)
                  (setq percent (+ 5 percent)))))))
      (message "tabify-indentation: done"))))

(defun joel-underline ()
  "Underline the previous line.
Use `=' characters if the previous line begins with `* '. Otherwise use `-'
characters."
  (interactive)
  (save-excursion
    (let (underline-char
          line-length)
      (beginning-of-line)
      (if (looking-at "\\* ")
          (setq underline-char ?=)
        (setq underline-char ?-))
      (let ((beginning-point (point)))
        (end-of-line)
        (setq line-length (- (point) beginning-point)))
      (beginning-of-line 2)
      (if (eq (following-char) underline-char)
      (let ((beg (point)))
        (forward-line)
        (delete-region beg (point))))
      (insert (make-string line-length underline-char) ?\n))))

(defun insert-horizontal-separator (char)
  "Insert a horizontal separator.
Prompt for character to use.
First delete whitespace at end of line, then insert copies of character
until line extends to fill-column."
  (interactive "cSeparator character: ")
  (let ((line-length
         (save-excursion
           (if (looking-at "[ \t]*$")
               (delete-region (point) 
                              (progn (skip-chars-forward " \t") (point)))
             (progn
               (end-of-line)
               (delete-region (point) 
                              (progn (skip-chars-backward " \t") (point)))))
           (current-column))))
    (if (> fill-column line-length)
        (insert (make-string (- fill-column line-length) char)))))

(defun insert-matching-separator ()
  "Insert a matching separator."
  (interactive)
  (let (begin-text 
        string-endpoint)
    (save-excursion
      (re-search-backward " - BEGIN ")
      (end-of-line)
      (backward-word)
      (setq string-endpoint (point))
      (beginning-of-line)
      (setq begin-text (buffer-string (point) string-endpoint)))
    (insert (replace-in-string begin-text " - BEGIN " " - END "))
    (if (> fill-column (current-column))
        (insert (make-string (- fill-column (current-column)) ?^)))
    (beginning-of-line)))

(defun safe-delete-window ()
  "Delete the current window from the display.
If window is the only one on the frame, print an error message. (I created
this function because I was tired of accidentally deleting frames.)"
  (interactive)
  (if (eq (selected-window) (next-window))
      (error "Cannot delete the only window in this frame")
    (delete-window)))

(defun maybe-kill-emacs ()
  "Ask the user if she wants to exit emacs; if so, do it."
  (interactive)
  (if (y-or-n-p "Exit Emacs? ")
      (save-buffers-kill-emacs)))

(defun comment-out-region (beg end &optional arg)
  "Comment or uncomment each line in the region.

This function is identical to comment-region, but it first sets the
comment-begin string to two copies of the first character in comment-begin, 
or '##' if comment-begin is nil."
  (interactive "r\nP")
  (let ((comment-start
         (if (eq comment-start nil)
             "##"
           (make-string 2 (elt comment-start 0)))))
    (comment-region beg end arg)))

(defun joel-comment-region (beg end &optional arg)
  "Comment or uncomment each line in the region.

With just C-u prefix arg, uncomment each line in region. Numeric
prefix arg ARG means use ARG comment characters. If ARG is negative,
delete that many comment characters instead.

Comments are terminated on each line, even for syntax in which newline
does not end the comment. Blank lines get empty comments.

The region is untabified before comment characters are added.

Bug (?): When comment-start is `// ' and this function is called with
a negative argument, it does not modify lines that contain only `//'."

  ;; (a modified version of comment-region from simple.el)
  (interactive "r\nP")
  (or comment-start (error "No comment syntax is defined"))
  (if (> beg end) (let (mid) (setq mid beg beg end end mid)))
  (save-excursion
    (save-restriction
      (let ((cs comment-start) (ce comment-end)
            numarg)
        (if (consp arg) (setq numarg t)
          (setq numarg (prefix-numeric-value arg))
          ;; For positive arg > 1, replicate the comment delims now,
          ;; then insert the replicated strings just once.
          (while (> numarg 1)
            (setq cs (concat cs comment-start)
                  ce (concat ce comment-end))
            (setq numarg (1- numarg))))
        ;; Loop over all lines from BEG to END.
        (narrow-to-region beg end)
        (goto-char beg)
        (if (or (eq numarg t) (< numarg 0)) ()
          (untabify beg end))
;          ;; untabify before adding comment characters (from untabify.el)
;          (while (search-forward "\t" nil t)	; faster than re-search
;            (let ((tab-beg (point))
;                  (column (current-column))
;                  (indent-tabs-mode nil))
;              (skip-chars-backward "\t" start)
;              (delete-region tab-beg (point))
;              (indent-to column)))
;        (goto-char beg)
        (while (not (eobp))
          (if (or (eq numarg t) (< numarg 0))
              (progn
                ;; Delete comment start from beginning of line.
                (if (eq numarg t)
                    (while (looking-at (regexp-quote cs))
                      (delete-char (length cs)))
                  (let ((count numarg))
                    (while (and (> 1 (setq count (1+ count)))
                                (looking-at (regexp-quote cs)))
                      (delete-char (length cs)))))
                ;; Delete comment end from end of line.
                (if (string= "" ce)
                    nil
                  (if (eq numarg t)
                      (progn
                        (end-of-line)
                        ;; This is questionable if comment-end ends in
                        ;; whitespace.  That is pretty brain-damaged,
                        ;; though.
                        (skip-chars-backward " \t")
                        (if (and (>= (- (point) (point-min)) (length ce))
                                 (save-excursion
                                   (backward-char (length ce))
                                   (looking-at (regexp-quote ce))))
                            (delete-char (- (length ce)))))
                    (let ((count numarg))
                      (while (> 1 (setq count (1+ count)))
                        (end-of-line)
                        ;; This is questionable if comment-end ends in
                        ;; whitespace.  That is pretty brain-damaged though
                        (skip-chars-backward " \t")
                        (save-excursion
                          (backward-char (length ce))
                          (if (looking-at (regexp-quote ce))
                              (delete-char (length ce))))))))
                (forward-line 1))
            ;; Insert at beginning and at end.
            (insert cs)
            (if (string= "" ce) ()
              (end-of-line)
              (insert ce))
            (search-forward "\n" nil 'move)))))))


(defvar truncation-string "..."
  "String used to indicate that a line has been truncated.")

(defun truncate-lines (beg end &optional arg)
  "Truncate lines in a region that are too long.
Numeric prefix arg specifies the maximum acceptable line length. (If none is 
specified, use the value of fill-column.)
The variable truncation-string is inserted at the end of each truncated line
to show that it has been truncated."
  (interactive "r\np")
  (save-excursion
    (save-restriction
      (let (trunc-column)
        (if arg
            (setq trunc-column arg)
          (setq trunc-column fill-column))
        (print arg)
        (narrow-to-region beg end)
        (goto-char beg)
        
        (while (not (eobp))
          (end-of-line)
          (if (> (current-column) trunc-column)
              (let ((line-end (point)))
                (move-to-column (- trunc-column (length truncation-string)))
                (delete-region (point) line-end)
                (insert-string truncation-string)))
          (forward-line 1))))))
  
(defun duplicate-with-numbers (beg end copy-count)
  "Make multiple copies of the region with increasing numbers.
Assume that the first string of digits in the region is the 'number'
of the region."
  (interactive "r\nNNumber of copies: ")
  (save-excursion
    (save-restriction
      (goto-char beg)
      (let* ((first-num-string
             (if (re-search-forward "[0-9]+" end t)
                 (match-string 0)
               (error "no number found in region")))
            (copy-num (string-to-int first-num-string))
            (copy-num-sentinel (+ copy-num copy-count))
            (region-string (buffer-string beg end)))
        (goto-char end)
        (setq copy-num (1+ copy-num))
        (while (< copy-num copy-num-sentinel)
          (insert (replace-in-string region-string 
                                     first-num-string 
                                     (int-to-string copy-num) 
                                     'literal))
          (setq copy-num (1+ copy-num)))))))


(defun toggle-tab-width (arg)
  "Change tab width and make sure TAB key is using real tabs."
  (interactive "p")
  (setq tab-width (cond ((> arg 1) arg)
                        ((eq tab-width 8) 4)
                        (t 8)))
  (setq indent-tabs-mode t)
  (if (eq (local-key-binding "\C-i") 'tab-to-tab-stop)
      (setq tab-stop-list (range tab-width 121 tab-width))))

(defun set-basic-offset (arg)
  "Prompt user for a new value for the basic offset.
Just set all the basic offsets, regardless of mode."
  (interactive "NNew basic offset: ")
  (setq c-basic-offset arg)
  (setq ksh-indent arg))


;;(defun find-files (dirname beg end)
;;  "Visit files listed in the region; each line should name a file.

;;When called with a numeric prefix argument (C-u), prompt the user for
;;the name of the working directory to open each file from."
;;  (interactive "DWorking directory: \nr")
;;  (save-excursion
;;    (save-restriction
;;      (let (default-directory)
;;        (cd dirname)
;;        (narrow-to-region beg end)
;;        (goto-char beg)
        
;;        (while (not (eobp))
;;          (let ((line-beg (point)))
;;            (end-of-line)
;;            (find-file (buffer-string line-beg (point))))
;;          (forward-line 1))))))
  
(defun find-files (beg end)
  "Visit files listed in the region; each line should name a file."
  (interactive "r")
  (save-excursion
    (save-restriction
      (narrow-to-region beg end)
      (goto-char beg)
        
      (while (not (eobp))
        (let ((line-beg (point)))
          (end-of-line)
          (find-file-noselect (buffer-string line-beg (point))))
        (forward-line 1)))))
  
(defun insert-total-time ()
  "Add all the mm:ss times in the preceding paragraph, and insert the total."
  (interactive)

  ;; delete current line
  (beginning-of-line)
  (delete-region (point) (progn (end-of-line) (point)))

  (let ((para-end (point)) (total 0) mm ss)
    ;; add up times
    (save-excursion
      (backward-paragraph)
      (while (re-search-forward "\\([0-9]+\\):\\([0-9][0-9]\\)" para-end t)
        (setq mm (string-to-number (match-string 1)))
        (setq ss (string-to-number (match-string 2)))
        (setq total (+ total (* mm 60) ss))))
    ;; insert total
    (insert (format "%3d:%02d" (/ total 60) (% total 60)))))


(defalias 'add-prototype (read-kbd-macro
"C-s C-j { 2*<C-b> C-r 2*<C-j> 2*<C-f> C-x C-x M-w C-x o C-y ; 2*RET C-x o C-s
C-j { C-s 2*<C-b> C-r 2*<C-j> 2*<C-f>"))


;; Gave up on this. It looked to complicated.
;;
;; (defun query-translate (from-strings to-strings)
;;   "Translate each element in FROM-STRINGS to an element in TO-STRINGS.
;; Both arguments must contain the same number of strings, seperated by spaces.
;; This command works like `query-replace' except that each element in
;; FROM-STRINGS is replaced with the corresponding element in TO-STRINGS.
;; 
;; Non-interactively, FROM-STRINGS and TO-STRINGS may lists of strings."
;;   (interactive
;;    (let (from to)
;;      (setq from (read-from-minibuffer "Query translate: "
;;                                       nil nil nil
;;                                       'query-replace-history)))
;;      (setq to (read-from-minibuffer (format "Query translate %s to: " from)
;;                                     nil nil nil
;;                                     'query-replace-history))
;;      (list from to)))
;;   (let (from to)
;;     (if (listp from-strings)
;;         (setq from from-strings)
;;       (setq from (split-string from-strings " ")))
;;     (if (listp from-strings)
;;         (setq from from-strings)
;;       (setq from (split-string from-strings " ")))
;;     (if (/= (length from) (length to))
;;         (error
;;      
;;       (while (/= (length from-strings) 0)
;;         (if (string-match " " from-strings)
;;             (setq from
;;                   (append from (list (substring 
;;                                       from-strings 
;;                                       0 (string-match " " from-strings))))
;;                   from-strings (substring 
;;                                 from-strings
;;                                 (1+ (string-match " " from-strings))))
;;           (setq from (append from (list from-strings))
;;                 from-strings ""))))
;;     (perform-replace regexp from t t nil arg)))


(global-auto-revert-mode 't)

;; "Tab" key shouldn't insert tab characters
(setq-default indent-tabs-mode nil)

(setq sentence-end-double-space nil)

(setq-default fill-column 76)

(setq-default tab-stop-list (range 4 121 4))

;;;=========================================================================
;;; python-mode customization

(defun my-python-mode-hook ()
  (auto-fill-mode +1)
  (font-lock-mode +1)

  (setq tab-width 8)
  (setq indent-tabs-mode nil)

;;    ;; Use 4-column tabs in order to comply with Starcat test coding
;;    ;; standards.
;;    (setq tab-width 4)
;;    (setq indent-tabs-mode t)))

  (define-key python-mode-map "\M-\C-m" 'indent-new-comment-line)
  )

(add-hook 'python-mode-hook 'my-python-mode-hook)


(define-key global-map "\C-ca" 'add-prototype)
(define-key global-map "\C-cb" 'joel-cleanup-buffer)
(define-key global-map "\C-cc" 'comment-out-region)
(define-key global-map "\C-cd" 'copy-region-as-kill)  ; "duplicate"
(define-key global-map "\C-ce" 'insert-matching-separator)
(define-key global-map "\C-cf" 'auto-fill-mode)
(define-key global-map "\C-ch" "\^c.\^khwad\^j\
\^cvindent-tabs-mode\^jnil\^j\
\^cvtab-width\^j8\^j")
(define-key global-map "\C-cj" 'japanese-font-setup-switch)
(define-key global-map "\C-cl" 'font-lock-fontify-buffer)
(define-key global-map "\C-cm" 'find-files)
(define-key global-map "\C-co" 'set-basic-offset)
(define-key global-map "\C-cr" 'reset-frame-size)
(define-key global-map "\C-cs" 'insert-horizontal-separator)
(define-key global-map "\C-ct" 'toggle-tab-width)
(define-key global-map "\C-cu" 'joel-underline)
(define-key global-map "\C-cv" 'set-variable)
(define-key global-map "\C-cw" 'cleanup-space-buffer-or-region)
(define-key global-map "\C-cxt" 'rebind-tab)
(define-key global-map "\C-cxx" 'font-setup-switch)

;; Make some built-in commands less error prone.
(define-key global-map "\C-x\C-c" 'maybe-kill-emacs)
(define-key global-map "\C-x0" 'safe-delete-window)
