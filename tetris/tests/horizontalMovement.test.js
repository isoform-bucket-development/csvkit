/**
 * Test Suite: Horizontal Movement
 *
 * Tests horizontal movement of tetrominoes with proper collision detection
 * as required by REQ-4 (move left/right) and REQ-16 (collision detection).
 */

const { GameBoard, BOARD_WIDTH, BOARD_HEIGHT, EMPTY_CELL } = require('../src/gameBoard');
const { Tetromino, createTetromino, TETROMINO_TYPES } = require('../src/tetromino');
const { ActivePiece, InputHandler, CONTROLS } = require('../src/piece');

describe('Horizontal Movement', () => {
  let board;
  let activePiece;

  beforeEach(() => {
    board = new GameBoard();
  });

  describe('Test Case 1: Move piece left from column 5 to column 4', () => {
    test('Piece at column 5 moves to column 4 when moveLeft is called', () => {
      // Create an active piece (T-piece for testing) at column 5
      const tetromino = createTetromino('T');
      activePiece = new ActivePiece(tetromino, board, 0, 5);

      const initialCol = activePiece.getColumn();
      expect(initialCol).toBe(5);

      // Move left
      const moved = activePiece.moveLeft();

      expect(moved).toBe(true);
      expect(activePiece.getColumn()).toBe(4);
    });
  });

  describe('Test Case 2: Move piece right from column 5 to column 6', () => {
    test('Piece at column 5 moves to column 6 when moveRight is called', () => {
      // Create an active piece at column 5
      const tetromino = createTetromino('T');
      activePiece = new ActivePiece(tetromino, board, 0, 5);

      const initialCol = activePiece.getColumn();
      expect(initialCol).toBe(5);

      // Move right
      const moved = activePiece.moveRight();

      expect(moved).toBe(true);
      expect(activePiece.getColumn()).toBe(6);
    });
  });

  describe('Test Case 3: Wall collision - left boundary', () => {
    test('Piece at column 0 remains at column 0 when moveLeft is called (wall collision)', () => {
      // Create an active piece at column 0 (left edge)
      const tetromino = createTetromino('O'); // O-piece is 2 wide
      activePiece = new ActivePiece(tetromino, board, 0, 0);

      const initialCol = activePiece.getColumn();
      expect(initialCol).toBe(0);

      // Attempt to move left - should fail due to wall collision
      const moved = activePiece.moveLeft();

      expect(moved).toBe(false);
      expect(activePiece.getColumn()).toBe(0);
    });

    test('Piece cannot move beyond left wall regardless of piece type', () => {
      // Test with I-piece (4 wide)
      const iPiece = createTetromino('I');
      const activePieceI = new ActivePiece(iPiece, board, 0, 0);

      expect(activePieceI.moveLeft()).toBe(false);
      expect(activePieceI.getColumn()).toBe(0);
    });
  });

  describe('Test Case 4: Wall collision - right boundary', () => {
    test('Piece at rightmost valid position remains there when moveRight is called (wall collision)', () => {
      // O-piece is 2 wide, so at column 8 it occupies columns 8-9
      // Column 9 would put it at 9-10, which is out of bounds
      const tetromino = createTetromino('O');
      activePiece = new ActivePiece(tetromino, board, 0, 8);

      // Attempt to move right - should fail due to wall collision
      const moved = activePiece.moveRight();

      expect(moved).toBe(false);
      expect(activePiece.getColumn()).toBe(8);
    });

    test('I-piece at column 6 cannot move right (occupies 6-9, moving would exceed boundary)', () => {
      // I-piece is 4 wide, at column 6 it occupies columns 6-9
      const iPiece = createTetromino('I');
      const activePieceI = new ActivePiece(iPiece, board, 0, 6);

      expect(activePieceI.moveRight()).toBe(false);
      expect(activePieceI.getColumn()).toBe(6);
    });

    test('T-piece at column 7 can move right to column 8 but not beyond', () => {
      // T-piece is 3 wide, at column 7 it occupies 7-9
      // At column 8 it would still fit (8-10 is out, so column 7 is the max)
      const tPiece = createTetromino('T');
      const activePieceT = new ActivePiece(tPiece, board, 0, 7);

      // Can't move right from column 7 (T-piece spans 3 columns: 7, 8, 9)
      expect(activePieceT.moveRight()).toBe(false);
      expect(activePieceT.getColumn()).toBe(7);
    });
  });

  describe('Test Case 5: Alternative controls - A key for left movement', () => {
    test('A key triggers left movement', () => {
      const tetromino = createTetromino('T');
      activePiece = new ActivePiece(tetromino, board, 0, 5);

      const inputHandler = new InputHandler(activePiece);

      // Simulate A key press
      inputHandler.handleKeyDown({ key: 'a' });

      expect(activePiece.getColumn()).toBe(4);
    });

    test('Uppercase A key also triggers left movement', () => {
      const tetromino = createTetromino('T');
      activePiece = new ActivePiece(tetromino, board, 0, 5);

      const inputHandler = new InputHandler(activePiece);

      // Simulate A key press (uppercase)
      inputHandler.handleKeyDown({ key: 'A' });

      expect(activePiece.getColumn()).toBe(4);
    });
  });

  describe('Test Case 6: Alternative controls - D key for right movement', () => {
    test('D key triggers right movement', () => {
      const tetromino = createTetromino('T');
      activePiece = new ActivePiece(tetromino, board, 0, 5);

      const inputHandler = new InputHandler(activePiece);

      // Simulate D key press
      inputHandler.handleKeyDown({ key: 'd' });

      expect(activePiece.getColumn()).toBe(6);
    });

    test('Uppercase D key also triggers right movement', () => {
      const tetromino = createTetromino('T');
      activePiece = new ActivePiece(tetromino, board, 0, 5);

      const inputHandler = new InputHandler(activePiece);

      // Simulate D key press (uppercase)
      inputHandler.handleKeyDown({ key: 'D' });

      expect(activePiece.getColumn()).toBe(6);
    });
  });

  describe('Arrow key controls', () => {
    test('ArrowLeft key triggers left movement', () => {
      const tetromino = createTetromino('T');
      activePiece = new ActivePiece(tetromino, board, 0, 5);

      const inputHandler = new InputHandler(activePiece);

      // Simulate left arrow key press
      inputHandler.handleKeyDown({ key: 'ArrowLeft' });

      expect(activePiece.getColumn()).toBe(4);
    });

    test('ArrowRight key triggers right movement', () => {
      const tetromino = createTetromino('T');
      activePiece = new ActivePiece(tetromino, board, 0, 5);

      const inputHandler = new InputHandler(activePiece);

      // Simulate right arrow key press
      inputHandler.handleKeyDown({ key: 'ArrowRight' });

      expect(activePiece.getColumn()).toBe(6);
    });
  });

  describe('Piece collision with placed blocks', () => {
    test('Piece cannot move left into placed block', () => {
      // Place a block at row 0, column 4
      board.setCellAt(0, 4, 1);
      board.setCellAt(1, 4, 1);

      const tetromino = createTetromino('O'); // O-piece is 2x2
      activePiece = new ActivePiece(tetromino, board, 0, 5);

      // Attempt to move left - should fail due to collision with placed block
      const moved = activePiece.moveLeft();

      expect(moved).toBe(false);
      expect(activePiece.getColumn()).toBe(5);
    });

    test('Piece cannot move right into placed block', () => {
      // Place a block at row 0, column 7
      board.setCellAt(0, 7, 1);
      board.setCellAt(1, 7, 1);

      const tetromino = createTetromino('O'); // O-piece is 2x2
      activePiece = new ActivePiece(tetromino, board, 0, 5);

      // Attempt to move right - should fail due to collision with placed block
      const moved = activePiece.moveRight();

      expect(moved).toBe(false);
      expect(activePiece.getColumn()).toBe(5);
    });
  });

  describe('Multiple consecutive movements', () => {
    test('Piece can move left multiple times until hitting wall', () => {
      const tetromino = createTetromino('O');
      activePiece = new ActivePiece(tetromino, board, 0, 5);

      // Move left 5 times - should stop at column 0
      for (let i = 0; i < 5; i++) {
        activePiece.moveLeft();
      }

      expect(activePiece.getColumn()).toBe(0);
    });

    test('Piece can move right multiple times until hitting wall', () => {
      const tetromino = createTetromino('O');
      activePiece = new ActivePiece(tetromino, board, 0, 5);

      // Move right multiple times - O-piece (2 wide) should stop at column 8
      for (let i = 0; i < 5; i++) {
        activePiece.moveRight();
      }

      expect(activePiece.getColumn()).toBe(8);
    });
  });

  describe('ActivePiece position methods', () => {
    test('getRow returns correct row', () => {
      const tetromino = createTetromino('T');
      activePiece = new ActivePiece(tetromino, board, 5, 3);

      expect(activePiece.getRow()).toBe(5);
    });

    test('getColumn returns correct column', () => {
      const tetromino = createTetromino('T');
      activePiece = new ActivePiece(tetromino, board, 5, 3);

      expect(activePiece.getColumn()).toBe(3);
    });

    test('getAbsoluteCells returns correct board positions', () => {
      const tetromino = createTetromino('O'); // 2x2 at [0,0],[0,1],[1,0],[1,1]
      activePiece = new ActivePiece(tetromino, board, 2, 3);

      const cells = activePiece.getAbsoluteCells();

      // O-piece cells relative to origin, offset by row 2, col 3
      expect(cells).toContainEqual([2, 3]);
      expect(cells).toContainEqual([2, 4]);
      expect(cells).toContainEqual([3, 3]);
      expect(cells).toContainEqual([3, 4]);
    });
  });

  describe('CONTROLS constant', () => {
    test('CONTROLS defines left movement keys', () => {
      expect(CONTROLS.LEFT).toContain('ArrowLeft');
      expect(CONTROLS.LEFT).toContain('a');
      expect(CONTROLS.LEFT).toContain('A');
    });

    test('CONTROLS defines right movement keys', () => {
      expect(CONTROLS.RIGHT).toContain('ArrowRight');
      expect(CONTROLS.RIGHT).toContain('d');
      expect(CONTROLS.RIGHT).toContain('D');
    });
  });
});
