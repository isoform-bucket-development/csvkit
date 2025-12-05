/**
 * Test Suite: Game Board Initialization
 *
 * This test suite verifies that the game board initializes correctly with proper
 * dimensions (10x20) and empty state as required by REQ-1.
 */

const { GameBoard, BOARD_WIDTH, BOARD_HEIGHT, EMPTY_CELL } = require('../src/gameBoard');

describe('Game Board Initialization', () => {
  let board;

  beforeEach(() => {
    board = new GameBoard();
  });

  describe('Test Case 1: Board Dimensions', () => {
    test('should initialize board with 10 columns', () => {
      expect(board.getWidth()).toBe(10);
      expect(BOARD_WIDTH).toBe(10);
    });

    test('should initialize board with 20 rows', () => {
      expect(board.getHeight()).toBe(20);
      expect(BOARD_HEIGHT).toBe(20);
    });

    test('should have grid with exactly 20 rows', () => {
      const grid = board.getGrid();
      expect(grid.length).toBe(20);
    });

    test('should have each row with exactly 10 columns', () => {
      const grid = board.getGrid();
      grid.forEach((row, index) => {
        expect(row.length).toBe(10);
      });
    });
  });

  describe('Test Case 2: Empty Cell State', () => {
    test('should have all 200 cells initially empty', () => {
      const grid = board.getGrid();
      let emptyCellCount = 0;

      for (let row = 0; row < 20; row++) {
        for (let col = 0; col < 10; col++) {
          if (grid[row][col] === EMPTY_CELL) {
            emptyCellCount++;
          }
        }
      }

      expect(emptyCellCount).toBe(200);
    });

    test('should return empty cell value for any valid position', () => {
      // Check corners
      expect(board.getCellAt(0, 0)).toBe(EMPTY_CELL);
      expect(board.getCellAt(0, 9)).toBe(EMPTY_CELL);
      expect(board.getCellAt(19, 0)).toBe(EMPTY_CELL);
      expect(board.getCellAt(19, 9)).toBe(EMPTY_CELL);

      // Check center
      expect(board.getCellAt(10, 5)).toBe(EMPTY_CELL);
    });

    test('should have isEmpty method returning true for new board', () => {
      expect(board.isEmpty()).toBe(true);
    });

    test('EMPTY_CELL constant should be defined and equal to 0', () => {
      expect(EMPTY_CELL).toBe(0);
    });
  });

  describe('Test Case 3: Visual Grid Rendering', () => {
    test('should have a render method', () => {
      expect(typeof board.render).toBe('function');
    });

    test('should render grid to a canvas context', () => {
      // Create a mock canvas context
      const mockContext = {
        fillStyle: '',
        strokeStyle: '',
        fillRect: jest.fn(),
        strokeRect: jest.fn(),
        clearRect: jest.fn(),
        beginPath: jest.fn(),
        moveTo: jest.fn(),
        lineTo: jest.fn(),
        stroke: jest.fn()
      };

      // Should not throw an error
      expect(() => board.render(mockContext)).not.toThrow();
    });

    test('should render with clear boundaries (grid lines)', () => {
      const mockContext = {
        fillStyle: '',
        strokeStyle: '',
        fillRect: jest.fn(),
        strokeRect: jest.fn(),
        clearRect: jest.fn(),
        beginPath: jest.fn(),
        moveTo: jest.fn(),
        lineTo: jest.fn(),
        stroke: jest.fn()
      };

      board.render(mockContext);

      // Should have cleared the canvas first
      expect(mockContext.clearRect).toHaveBeenCalled();
    });

    test('should have configurable cell size', () => {
      expect(board.getCellSize()).toBeGreaterThan(0);
    });

    test('should calculate total board pixel dimensions correctly', () => {
      const cellSize = board.getCellSize();
      expect(board.getPixelWidth()).toBe(10 * cellSize);
      expect(board.getPixelHeight()).toBe(20 * cellSize);
    });
  });

  describe('Board State Management', () => {
    test('should allow resetting the board to empty state', () => {
      // First, verify we can modify and then reset
      board.reset();
      expect(board.isEmpty()).toBe(true);
    });

    test('should return a copy of grid to prevent direct mutation', () => {
      const grid1 = board.getGrid();
      const grid2 = board.getGrid();

      // Should be equal but not the same reference
      expect(grid1).toEqual(grid2);
      expect(grid1).not.toBe(grid2);
    });
  });
});
