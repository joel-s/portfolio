; -*- Mode: Emacs-Lisp -*-

; SCCS ID: "%Z%%M%	%I%	%E% SMI"

;;; Kludge to make hexl mode work in xemacs
(defun get-coding-system (arg)
  arg)


;;; Hack for working with mule...
(if (string-match "XEmacs" emacs-version)
    ()
  (set-background-color "gray10")
  (set-face-background 'default "gray10")
  (set-cursor-color "red")
  (stop-processing-this-file)  ; intentional error
  )


;; Note: the following will cause problems if ~/lib/xemacs contains any
;; files which have the same names as xemacs built-ins (but are not intended 
;; to replace them). I learned this the hard way with macros.el.

(setq load-path (cons "/home/joelsu/lib/xemacs" load-path))

(require 'font-lock)
(require 'vc)


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

(defvar microscroll-lines 1
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


(defvar font-setup-font-number 0
  "The number of the currently selected font setup.")

(defvar font-setup-font-list
  [["-*-lucidatypewriter-medium-r-*-*-*-100-*-*-*-*-iso8859-*"
    "-*-lucidatypewriter-medium-r-*-*-*-100-*-*-*-*-iso8859-*"
    "-*-lucidatypewriter-bold-r-*-*-*-100-*-*-*-*-iso8859-*"
    "-*-lucidatypewriter-bold-r-*-*-*-100-*-*-*-*-iso8859-*"]
   ["-*-lucidatypewriter-medium-r-*-*-*-120-*-*-*-*-iso8859-*"
    "-*-lucidatypewriter-medium-r-*-*-*-120-*-*-*-*-iso8859-*"
    "-*-lucidatypewriter-bold-r-*-*-*-120-*-*-*-*-iso8859-*"
    "-*-lucidatypewriter-bold-r-*-*-*-120-*-*-*-*-iso8859-*"]
   ["-adobe-courier-medium-r-*-*-*-100-*-*-*-*-iso8859-*"
    "-adobe-courier-medium-o-*-*-*-100-*-*-*-*-iso8859-*"
    "-adobe-courier-bold-r-*-*-*-100-*-*-*-*-iso8859-*" 
    "-adobe-courier-bold-o-*-*-*-100-*-*-*-*-iso8859-*"]]
  "Array of font setups.
Each element is an array of four font names. These are assigned to the faces
normal, bold, italic, and bold-italic.")

(defun font-setup-switch ()
  "Select the next font setup."
  (interactive)
  (setq font-setup-font-number (1+ font-setup-font-number))
  (if (>= font-setup-font-number (length font-setup-font-list))
      (setq font-setup-font-number 0))
  (let ((fonts (aref font-setup-font-list font-setup-font-number)))
    (set-face-font 'default (aref fonts 0))
    (set-face-font 'italic (aref fonts 1))
    (set-face-font 'bold (aref fonts 2))
    (set-face-font 'bold-italic (aref fonts 3))
    (setq ps-build-face-reference 't)))


;;(defvar japanese-font-list
;;  [["-misc-fixed-medium-r-normal--14-130-75-75-c-140-jisx0208.1983-0"]
;;   ["-jis-fixed-medium-r-normal--16-150-75-75-c-160-jisx0208.1983-0"]
;;   ["-jis-fixed-medium-r-normal--24-230-75-75-c-240-jisx0208.1983-0"]]
;;  "Array of Japanese font setups.")
    


(defvar japanese-font-list
  [[(((mule-fonts) . "-misc-fixed-medium-r-normal-*-14-*-*-*-c-*-jisx0208.1983-0")
      ((mule-fonts) . "-misc-fixed-medium-r-normal-*-14-*-*-*-c-*-jisx0201.1976-0")
      ((x) . "-misc-fixed-medium-r-normal-*-14-*-*-*-c-*-iso8859-1"))]
   [(((mule-fonts) . "-jis-fixed-medium-r-normal-*-16-*-*-*-c-*-jisx0208.1983-0")
      ((mule-fonts) . "-sony-fixed-medium-r-normal-*-16-*-*-*-c-*-jisx0201.1976-0")
      ((x) . "-sony-fixed-medium-r-normal-*-16-*-*-*-c-*-iso8859-1"))]
   [(((mule-fonts) . "-jis-fixed-medium-r-normal-*-24-*-*-*-c-*-jisx0208.1983-0")
      ((mule-fonts) . "-sony-fixed-medium-r-normal-*-24-*-*-*-c-*-jisx0201.1976-0")
      ((x) . "-sony-fixed-medium-r-normal-*-24-*-*-*-c-*-iso8859-1"))]]
  "Array of Japanese font setups.")

(defun japanese-font-setup-switch ()
  "Select the next font setup."
  (interactive)
  (setq font-setup-font-number (1+ font-setup-font-number))
  (if (>= font-setup-font-number (length japanese-font-list))
      (setq font-setup-font-number 0))
  (let ((fonts (aref japanese-font-list font-setup-font-number)))
    (set-face-font 'default (aref fonts 0))
    (set-face-font 'italic (aref fonts 0))
    (set-face-font 'bold (aref fonts 0))
    (set-face-font 'bold-italic (aref fonts 0))
    (setq ps-build-face-reference 't)))


    


;; (note to self: a few more functions exist, mostly specific to C coding;
;; see ~/emacs/fromdotemacs.el)


;;;=========================================================================
;;; Misc. global customization

(pending-delete +1)

;; Hide defualt toolbar
(set-default-toolbar-position 'right)
(set-specifier right-toolbar-width 0)

;; If the user attempts to save a file that does not end in a newline, ask
;; the user whether or not to add a newline.
(setq require-final-newline 'prompt-user)

;; Don't beep!
;;(setq visible-bell t)

;; Rectangular cursor (it's much easier to see)
(setq-default bar-cursor nil)

;; "Tab" key shouldn't insert tab characters
(setq-default indent-tabs-mode nil)

;; When in X, delete key should delete characters after the point
;; (i.e., backspace /= control-H)
(if (not (equal (console-type) 'tty))
    (setq delete-key-deletes-forward t))

(setq sentence-end-double-space nil)

(setq-default fill-column 76)

(setq-default tab-stop-list (range 4 121 4))

(setq default-major-mode 'text-mode)

(setq vc-default-back-end 'SCCS)

;;(auto-compression-mode +1)  ; this doesn't work in XEmacs 20.3b
(toggle-auto-compression +1)


;; customize tab-stop-list
;; ...

;;(defun my-find-file-hook ()
;;  (auto-fill-mode +1)
;;  (font-lock-mode +1))
;;
;;(add-hook 'find-file-hooks 'my-find-file-hook)

(setq interpreter-mode-alist
      (append '(("^#!.*ksh"	  . ksh-mode))
              interpreter-mode-alist))

;;;=========================================================================
;;; cc-mode customization

;; Open .h files in C++ mode
(setq auto-mode-alist
      (append '(("\\.ksh\\'" . ksh-mode) 
                ("/\\.\\(bash_\\)?\\(profile\\|login||logout\\)\\'" . ksh-mode)
                ("/\\.\\(ksh\\|bash\\)rc\\'" . ksh-mode)
;                ("\\.h\\'"  . c++-mode)
                )
              auto-mode-alist))

(require 'cc-mode)

(defconst hwad-c-style
  '((c-basic-offset . 2)
    (c-comment-only-line-offset . 0)
    (c-offsets-alist . ((statement-block-intro . +)
                        (substatement-open . 0)
                        (label . *)
                        (case-label . *)
                        (access-label . 0)
                        (statement-cont . +)))
    )
  "HWAD C programming style.
Basic indent is 2 spaces.")
(c-add-style "hwad" hwad-c-style)


(defconst benc-c-style
  '((c-basic-offset  . 8)
    (c-comment-only-line-offset . 0)
    (c-hanging-braces-alist . ((brace-list-open)
                               (brace-entry-open)
                               (substatement-open after)
                               (block-close . c-snug-do-while)))
    (c-cleanup-list . (brace-else-brace))
    (c-offsets-alist . ((statement-block-intro . +)
                        (knr-argdecl-intro     . 0)
                        (substatement-open     . 0)
                        (label                 . 0)
                        (statement-cont        . *)
                        (arglist-intro . *)
                        (arglist-cont . *)
                        (arglist-cont-nonempty . *)
                        (arglist-close . *)
                        ))
    )
  "The style Ben Chang uses, probably official Solaris style.")
(c-add-style "benc" benc-c-style)

;;(defconst joel-c-style
;;  '((c-basic-offset . 4)
;;    (c-comment-only-line-offset . 0)
;;    (c-offsets-alist . ((statement-block-intro . +)
;;                        (substatement-open . 0)
;;                        (label . *)
;;                        (case-label . *)
;;                        (access-label . 0)
;;                        (statement-cont . +)))
;;    )
;;  "Joel's C programming style.
;;Similar to ``stroustrup'', but labels are indented by 2 spaces.")

(defun my-c-mode-common-hook ()
  ;;(c-add-style "joel" joel-c-style t)
  ;;(c-toggle-hungry-state +1)

  (c-set-style "benc")
;;  (c-set-style "stroustrup")

  (auto-fill-mode +1)
  (font-lock-mode +1)

  ;; Using 8-column tabs in order to comply with SMS coding standards.
  (setq tab-width 8)
  (setq indent-tabs-mode t)

  ;; Tell cc-mode not to check for old-style (K&R) function declarations.
  ;; This speeds up indenting a lot.
  (setq c-recognize-knr-p nil)

  (define-key c-mode-base-map "\C-m" 'newline-and-indent)
  (define-key c-mode-base-map "\M-\C-m" 'c-indent-new-comment-line)
  (define-key c-mode-base-map "\C-j" 'newline)
;;  (define-key c-mode-base-map "\C-i" 'indent-according-to-mode)
  )

(add-hook 'c-mode-common-hook 'my-c-mode-common-hook)


;;;=========================================================================
;;; python-mode customization

(defun my-python-mode-hook ()
  (auto-fill-mode +1)
  (font-lock-mode +1)

  ;; Using 4-column tabs in order to comply with Starcat test coding
  ;; standards.
  (setq tab-width 4)
  (setq indent-tabs-mode t)
  (define-key py-mode-map "\M-\C-m" 'indent-new-comment-line)
  )

(add-hook 'python-mode-hook 'my-python-mode-hook)


;;;=========================================================================
;;; makefile-mode customization

(defun my-makefile-mode-hook ()
  (auto-fill-mode +1)
  (font-lock-mode +1)

  ;; Using 4-column tabs in order to comply with Starcat test coding
  ;; standards.
  (setq tab-width 4))

(add-hook 'makefile-mode-hook 'my-makefile-mode-hook)


;;;=========================================================================
;;; ksh-mode customization

(defun my-ksh-mode-hook ()
  (font-lock-mode +1)

  (setq ksh-indent 4)
  (setq ksh-group-offset -4)
  (setq ksh-brace-offset -4)
  (setq ksh-case-item-offset 0)
  (setq ksh-case-indent 4)
  (setq ksh-multiline-offset 2)

  (make-variable-buffer-local 'ksh-indent)

;;   ;; Using 4-column tabs in order to comply with Starcat test coding
;;   ;; standards.
;;   (setq tab-width 4)
;;   (setq indent-tabs-mode t)

  (setq tab-width 8)
  (setq indent-tabs-mode nil)

  (define-key ksh-mode-map "\C-m" 'newline-and-indent)
  (define-key ksh-mode-map "\C-\M-m" 'indent-new-comment-line)
  (define-key ksh-mode-map "\C-j" 'newline))

(add-hook 'ksh-mode-hook 'my-ksh-mode-hook)


;;;=========================================================================
;;; text-mode customization

(defun my-generic-hook ()
  (auto-fill-mode +1)
  (font-lock-mode +1))

(add-hook 'text-mode-hook 'my-generic-hook)


;;;=========================================================================
;;; dired-mode customization

(defun my-dired-mode-hook ()
  (define-key dired-mode-map [f2] "\C-uo")
  (define-key dired-mode-map [f3] 'scroll-other-window)
  (define-key dired-mode-map [f4] 'scroll-other-window-down))

(add-hook 'dired-mode-hook 'my-dired-mode-hook)


;;;=========================================================================
;;; html-mode customization

(defun my-html-mode-hook ()
   (auto-fill-mode +1)
   (font-lock-mode +1)

;;   ;; Using 4-column tabs in order to comply with Starcat test coding
;;   ;; standards. (Not compliant with SMS coding standards.)
;;   (setq tab-width 4)
   (setq indent-tabs-mode nil)

   (define-key html-mode-map "\C-i" 'tab-to-tab-stop)
   (define-key html-mode-map "\C-ci" 'sgml-indent-or-tab)
  
   )




;; (add-hook 'html-mode-hook 'my-html-mode-hook)


(setq-default ediff-window-setup-function 'ediff-setup-windows-plain)

;; (defun my-ediff-mode-hook ()
;;   (setq-default ediff-window-setup-function 'ediff-setup-windows-plain))



;;;=========================================================================
;;; Faces, colors, etc.

;; Set face properties; most of these cannot be set in Emacs resource file

(blink-cursor-mode 0)


;;(set-face-property 'default 'background "gray10")
;;(set-face-property 'default 'foreground "lightyellow")
;;(set-face-property 'text-cursor 'background "red")
;;;(set-face-property 'text-cursor 'foreground "gray10")

;;(set-face-property 'font-lock-comment-face 'foreground "lightblue2")
;;(make-face-italic 'font-lock-comment-face)
;;(set-face-property 'font-lock-doc-string-face 'foreground "lightblue2")
;;(make-face-italic 'font-lock-doc-string-face)
;;(set-face-property 'font-lock-string-face 'foreground "lightblue2")
;;(make-face-italic 'font-lock-string-face)

;;(set-face-property 'font-lock-keyword-face 'foreground "burlywood")

;;(set-face-property 'font-lock-function-name-face 'foreground "khaki")
;;(make-face-bold 'font-lock-function-name-face)

;;(set-face-property 'font-lock-type-face 'foreground "khaki")
;;(make-face-bold 'font-lock-type-face)

;;(set-face-property 'font-lock-variable-name-face 'foreground "lightyellow")

;;(set-face-property 'font-lock-preprocessor-face 'foreground "lightcyan2")
;;(make-face-bold 'font-lock-preprocessor-face)

;;(set-face-property 'font-lock-reference-face 'foreground "lightcyan2")
;;(make-face-bold 'font-lock-reference-face)

;;(require 'hyper-apropos)
;;(set-face-property 'hyper-apropos-documentation 'foreground "lightblue2")
;;(set-face-property 'hyper-apropos-hyperlink 'foreground "lightgoldenrod")

;;(set-face-property 'primary-selection 'background "darkcyan")

;;(set-face-property 'zmacs-region 'background "slateblue")
;;(set-face-property 'primary-selection 'background "slateblue")
;;(set-face-property 'secondary-selection 'background "darkslateblue")
;;(set-face-property 'isearch 'background "darkcyan")
;;(set-face-property 'highlight 'background "darkcyan")


(set-face-property 'default 'background "gray10")
(set-face-property 'default 'foreground "lightyellow")
(set-face-property 'text-cursor 'background "red")
;(set-face-property 'text-cursor 'foreground "gray10")

(set-face-parent 'font-lock-comment-face 'italic)
(set-face-property 'font-lock-comment-face 'foreground "lightblue2")

(set-face-parent 'font-lock-doc-string-face 'italic)
(set-face-property 'font-lock-doc-string-face 'foreground "lightblue2")

(set-face-parent 'font-lock-string-face 'italic)
(set-face-property 'font-lock-string-face 'foreground "lightblue2")

(set-face-property 'font-lock-keyword-face 'foreground "burlywood")

(set-face-parent 'font-lock-function-name-face 'bold)
(set-face-property 'font-lock-function-name-face 'foreground "khaki")

(set-face-parent 'font-lock-type-face 'bold)
(set-face-property 'font-lock-type-face 'foreground "khaki")

(set-face-property 'font-lock-variable-name-face 'foreground "lightyellow")

(set-face-parent 'font-lock-preprocessor-face 'bold)
(set-face-property 'font-lock-preprocessor-face 'foreground "lightcyan2")

(set-face-parent 'font-lock-reference-face 'bold)
(set-face-property 'font-lock-reference-face 'foreground "lightcyan2")

(require 'hyper-apropos)
(set-face-property 'hyper-apropos-documentation 'foreground "lightblue2")
(set-face-property 'hyper-apropos-hyperlink 'foreground "lightgoldenrod")

(set-face-property 'primary-selection 'background "darkcyan")

(set-face-property 'zmacs-region 'background "slateblue")
(set-face-property 'primary-selection 'background "slateblue")
(set-face-property 'secondary-selection 'background "darkslateblue")
(set-face-property 'isearch 'background "darkcyan")
(set-face-property 'highlight 'background "darkcyan")

;;;=========================================================================
;;; Key bindings

(define-key global-map [(shift down)] 'microscroll-up)
(define-key global-map [(shift up)] 'microscroll-down)

(define-key global-map [print] 'ps-spool-buffer-with-faces)
(define-key global-map [(control print)] 'ps-spool-region-with-faces)
(define-key global-map [(meta print)] 'ps-despool)

(define-key global-map [(meta escape) %] 'query-replace-regexp)

(defalias 'joel-cleanup-buffer
  (read-kbd-macro
   "C-SPC C-g C-x h M-x tabify-indentation RET C-x C-SPC C-c w"))

(defalias 'append-region-to-kill
  (read-kbd-macro "C-M-w M-x copy- region- as- kill RET"))

; works for printing japanese email in portrait orientation
(defalias 'htmlize-document (read-kbd-macro
"ESC < C-c w RET <up> ESC % C-q C-j RET C-q C-j < h4 > RET ! ESC < ESC % < h4 > C-q C-j RET < p > &nbsp; C-q C-j RET ! ESC < C-x C-f ~/p/eriko/template.html RET ESC < C-SPC 8*<down> <copy> C-x b RET <paste> ESC > RET C-x b RET ESC > C-SPC 2*<up> <copy> C-x b RET <paste>"))

; works for printing japanese email in landscape orientation
(defalias 'htmlize-document-big (read-kbd-macro
"ESC < C-c w RET <up> ESC % C-q C-j RET C-q C-j < h2 > RET ! ESC < ESC % < h2 > C-q C-j RET < p > &nbsp; C-q C-j RET ! ESC < C-x C-f ~/p/eriko/template.html RET ESC < C-SPC 8*<down> <copy> C-x b RET <paste> ESC > RET C-x b RET ESC > C-SPC 2*<up> <copy> C-x b RET <paste>"))

(defun copy-line-as-kill (&optional arg)
  "Similar to kill-line, but do not actually delete the text.
Without argument, copy the whole line, as if kill-whole-line were set."
  (interactive "P")
  (copy-region-as-kill
   (point)
   (save-excursion
     (if arg
         (forward-line (prefix-numeric-value arg))
       (if (eobp)
           (signal 'end-of-buffer nil))
       (forward-line 1))
     (point))))

(defalias 'bogosify-log-line
  (read-kbd-macro "C-a 4*<M-f> 2*SPC Info 5*SPC BOGUS> C-a <down>"))

(defun append-line-to-kill (&optional arg)
  "Similar to copy-line-as-kill, but append to the kill ring."
  (interactive "P")
  (setq last-command 'kill-region)
  (copy-line-as-kill arg))

(define-key global-map [f1] 'call-last-kbd-macro)
(define-key global-map [f2] 'append-line-to-kill)

(define-key global-map [f5] "\^xria")
(define-key global-map [f6] "\^xrib")
(define-key global-map [f7] "\^xric")
(define-key global-map [f8] "\^xrid")

(define-key global-map [f9] "\M--\C-xo")
(define-key global-map [f10] "\C-xo")

(define-key global-map "\M-s" 'center-line)
(define-key text-mode-map "\C-i" 'tab-to-tab-stop)

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

(defvar japanese-font 
  '(((mule-fonts) . "-jis-fixed-medium-r-normal-*-16-*-*-*-c-*-jisx0208.1983-0")
    ((mule-fonts) . "-sony-fixed-medium-r-normal-*-16-*-*-*-c-*-jisx0201.1976-0")
    ((x) . "-sony-fixed-medium-r-normal-*-16-*-*-*-c-*-iso8859-1"))
  "My favorite Japanese font.")

(if t
    ()
  (progn
    (set-face-font 'default 
                   '(((mule-fonts) . "-misc-fixed-medium-r-normal-*-14-*-*-*-c-*-jisx0208.1983-0")
                     ((mule-fonts) . "-misc-fixed-medium-r-normal-*-14-*-*-*-c-*-jisx0201.1976-0")
                     ((x) . "-misc-fixed-medium-r-normal-*-14-*-*-*-c-*-iso8859-1")))
    (set-face-font 'default "-misc-fixed-medium-r-normal-*-14-*-*-*-c-*-iso8859-1"))

  (progn
    (set-face-font 'default 
                   '(((mule-fonts) . "-jis-fixed-medium-r-normal-*-16-*-*-*-c-*-jisx0208.1983-0")
                     ((mule-fonts) . "-sony-fixed-medium-r-normal-*-16-*-*-*-c-*-jisx0201.1976-0")
                     ((x) . "-sony-fixed-medium-r-normal-*-16-*-*-*-c-*-iso8859-1")))
    (set-face-font 'default "-sony-fixed-medium-r-normal-*-16-*-*-*-c-*-iso8859-1"))
  (progn
    (set-face-font 'default 
                   '(((mule-fonts) . "-jis-fixed-medium-r-normal-*-24-*-*-*-c-*-jisx0208.1983-0")
                     ((mule-fonts) . "-sony-fixed-medium-r-normal-*-24-*-*-*-c-*-jisx0201.1976-0")
                     ((x) . "-sony-fixed-medium-r-normal-*-24-*-*-*-c-*-iso8859-1")))
    (set-face-font 'default "-sony-fixed-medium-r-normal-*-24-*-*-*-c-*-iso8859-1")))

(cond 
 ((featurep 'mule)

  (set-face-font 'default japanese-font)
  (set-face-font 'bold japanese-font)
  (set-face-font 'italic japanese-font)
  (set-face-font 'bold-italic japanese-font)
  (set-face-foreground 'bold "lightgoldenrod")

  ;; These settings from SKK readme file

  (global-set-key "\C-x\C-j" 'skk-mode)
  (global-set-key "\C-xj" 'skk-auto-fill-mode)
  (global-set-key "\C-xt" 'skk-tutorial)
  (autoload 'skk-mode "skk" nil t)
  (autoload 'skk-tutorial "skk-tut" nil t)
  (autoload 'skk-check-jisyo "skk-tools" nil t)
  (autoload 'skk-merge "skk-tools" nil t)
  (autoload 'skk-diff "skk-tools" nil t)
  
  (autoload 'skk-isearch-mode-setup "skk-isearch" nil t)
  (autoload 'skk-isearch-mode-cleanup "skk-isearch" nil t)
  (add-hook 'isearch-mode-hook
            (function (lambda ()
                        (and (boundp 'skk-mode) skk-mode
                             (skk-isearch-mode-setup)))))
  (add-hook 'isearch-mode-end-hook
            (function (lambda ()
                        (and (boundp 'skk-mode) skk-mode
                             (skk-isearch-mode-cleanup)
                             (skk-set-cursor-color-properly)))))

  ;; Fix certain faces so they do not specify a particular font.

;;  (require 'info)
;;  (require 'hyper-apropos)

;;  (mapcar
;;   (lambda (face)
;;     (cond
;;      ((and
;;        (stringp (cdadar (specifier-spec-list (face-font face))))
;;        (not (member (face-name face) '(default bold italic bold-italic)))
;;        (string-match "bold" (face-font-name face)))
;;       (remove-face-property face 'font)
;;       (set-face-parent face 'bold))))
;;   (list-faces))

  ))

;;(font-instance-properties (face-font-instance 'info-node))

;;(face-name 'info-node)


;;(member (face-name 'default) '(default bold italic bold-italic))

;;(specifier-instance (face-font 'font-lock-function-name-face) nil nil t)


;;(specifier-spec-list (face-font 'bold))
;;(specifier-spec-list (face-font 'info-node))
;;(specifier-spec-list (face-font 'font-lock-function-name-face))

;;(cdadar (specifier-spec-list (face-font 'info-node)))

;;(face-font 'font-lock-function-name-face)


;;(face-font 'default)
;;#<font-specifier global=("-jis-fixed-medium-r-normal--16-150-75-75-c-160-jisx0208.1983-0" ((x) . "-*-lucidatypewriter-medium-r-*-*-*-120-*-*-*-*-iso8859-*") ((mule-fonts) . "-*-fixed-medium-r-*--16-*-iso8859-1") ((mule-fonts) . "-*-fixed-medium-r-*--*-iso8859-1") ((mule-fonts) . "-*-fixed-medium-r-*--*-iso8859-2") ((mule-fonts) . "-*-fixed-medium-r-*--*-iso8859-3") ...) fallback=(((tty) . "normal") ((x) . "-*-courier-medium-r-*-*-*-120-*-*-*-*-iso8859-*") ((x) . "-*-courier-medium-r-*-*-*-120-*-*-*-*-iso8859-*") ((x) . "-*-courier-*-r-*-*-*-120-*-*-*-*-iso8859-*") ((x) . "-*-*-medium-r-*-*-*-120-*-*-m-*-iso8859-*") ((x) . "-*-*-medium-r-*-*-*-120-*-*-c-*-iso8859-*") ...) 0x1c9>

;;(font-instance-properties (face-font-instance 'default))
;;((COPYRIGHT . "from JIS X 9051-1984, by permission to use") (FONTNAME_REGISTRY . "") (FOUNDRY . "JIS") (FAMILY_NAME . "Fixed") (WEIGHT_NAME . "Medium") (SLANT . "R") (SETWIDTH_NAME . "Normal") (ADD_STYLE_NAME . "") (PIXEL_SIZE . 16) (POINT_SIZE . 150) (RESOLUTION_X . 75) (RESOLUTION_Y . 75) (SPACING . "C") (AVERAGE_WIDTH . 160) (CHARSET_REGISTRY . "JISX0208.1983") (CHARSET_ENCODING . "0") (FONT . "-JIS-Fixed-Medium-R-Normal--16-150-75-75-C-160-JISX0208.1983-0") (WEIGHT . 10) (RESOLUTION . 107) (X_HEIGHT . -1) (QUAD_WIDTH . 16))

;;(list-fonts "*")

(setq vm-mime-charset-font-alist
   '(
     ("iso-2022-jp" . "-*-lucidatypewriter-medium-r-*-*-*-120-*-*-*-*-iso8859-*")
    )
  )


;;; Cryptography

(setq crypt-encryption-type 'gpg
      crypt-confirm-password 't
      )

(require 'crypt++)


;; Recommended to make sure EOL translation does not affect compressed files
;; read by crypt++.
;;(modify-coding-system-alist 'file "\\.gz\\'" 'no-conversion)
;;(modify-coding-system-alist 'file "\\.Z\\'" 'no-conversion)
;;(modify-coding-system-alist 'file "\\.bz\\'" 'no-conversion)
;;(modify-coding-system-alist 'file "\\.bz2\\'" 'no-conversion)


;; Mail setup for work
;;(setq vm-folder-directory "~/Mail/")
;;(setq vm-primary-inbox "~/Mail/INBOX")
;;(setq vm-crash-box "~/Mail/INBOX.CRASH")
;;(setq vm-spool-files '("~/Mail/INBOX" "imap:postoffice.west:143:inbox:login:joelsu:*" "~/Mail/INBOX.CRASH"))
;;(setq vm-imap-expunge-after-retrieving nil)
;;(setq vm-delete-after-saving t)


;; Mail setup for home
(setq vm-folder-directory "~/Mail/")
(setq vm-primary-inbox "~/Mail/REMOTE")
(setq vm-crash-box "~/Mail/REMOTE.CRASH")
(setq vm-spool-files '("~/Mail/REMOTE" "imap:netmail.home.com:110:pass:joel.sullivan@home.com:*" "~/Mail/REMOTE.CRASH"))
;;(setq vm-imap-expunge-after-retrieving nil)
;;(setq vm-delete-after-saving t)
(setq vm-pop-expunge-after-retrieving nil)

(custom-set-variables
 '(user-mail-address "Joel.Sullivan@Sun.COM")
 '(load-home-init-file t t)
 '(query-user-mail-address nil)
 '(message-default-mail-headers "FCC: ~/Mail/Sent
")
 '(font-lock-verbose nil))
(custom-set-faces
 '(message-header-cc-face ((((class color) (background light)) (:foreground "lightgoldenrod"))))
 '(ediff-odd-diff-face-C ((((class color)) (:foreground "White" :background "Grey55"))))
 '(ediff-odd-diff-face-B ((((class color)) (:foreground "White" :background "Grey55"))))
 '(ediff-odd-diff-face-A ((((class color)) (:foreground "White" :background "Grey55"))))
 '(message-header-name-face ((((class color) (background light)) (:foreground "lightblue2"))))
 '(message-separator-face ((((class color) (background light)) (:foreground "red"))))
 '(message-header-to-face ((((class color) (background light)) (:foreground "lightgoldenrod" :bold t))))
 '(widget-field-face ((((class grayscale color) (background light)) (:background "gray55"))))
 '(ediff-even-diff-face-Ancestor ((((class color)) (:foreground "Black" :background "light grey"))))
 '(ediff-even-diff-face-B ((((class color)) (:foreground "Black" :background "light grey"))))
 '(ediff-odd-diff-face-Ancestor ((((class color)) (:foreground "White" :background "Grey55"))))
 '(message-header-newsgroups-face ((((class color) (background light)) (:foreground "burlywood" :bold t :italic t))))
 '(message-header-subject-face ((((class color) (background light)) (:foreground "burlywood" :bold t)))))


;; At end: import packages that sometimes fail
;(require 'ps-print)

